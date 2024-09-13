import os
from dotenv import load_dotenv
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pydantic import BaseModel
import nest_asyncio
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
import sqlalchemy
from src import database as db
from sqlalchemy.exc import DBAPIError
import requests
import json
import tempfile
from typing import List
import re
from fastapi import Form
import asyncio


# Load environment variables
load_dotenv()

# Apply nest_asyncio
nest_asyncio.apply()

# Set up router
router = APIRouter(
    prefix="/insert",
    tags=["insert"],
)

# Set up LlamaParse
llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
parser = LlamaParse(
    api_key=llamaparse_api_key,
    result_type="markdown"
)

# Hugging Face model setup
model_id = "intfloat/multilingual-e5-small"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}

def query(texts, name, author, source):
    for i in range(len(texts)):
        texts[i] = f" {name}, {author}, {source}, {texts[i]}"
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()

def split_into_sentences(text):
    return re.split(r'(?<=[.!?])\s+|\Z', text)

def create_chunks(text, max_words=380):
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_words = sentence.split()
        sentence_word_count = len(sentence_words)

        if current_word_count + sentence_word_count <= max_words:
            current_chunk.extend(sentence_words)
            current_word_count += sentence_word_count
        else:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = sentence_words
            current_word_count = sentence_word_count

            while current_word_count > max_words:
                chunks.append(' '.join(current_chunk[:max_words]))
                current_chunk = current_chunk[max_words:]
                current_word_count = len(current_chunk)

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

@router.post("/PDF")
async def update_times(name: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF file.")

    try:
        contents = await file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
        
        file_extractor = {".pdf": parser}
        documents = SimpleDirectoryReader(input_files=[temp_file_path], file_extractor=file_extractor).load_data()
        
        os.unlink(temp_file_path)
        
        if not documents:
            raise ValueError("No content extracted from PDF")
        
        text = "\n".join([doc.text for doc in documents])
        print("Parsed Text:")
        print(text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

    result = insertChunksWithLlamaParse(text=text, name=name, link=file.filename, source="PDF")

    return result

class InputText(BaseModel):
    name: str
    text: str
    source: str
    author: str = 'NULL'

@router.post("/text")
def update_times(input: InputText):
    result = insertChunksWithLlamaParse(input.text, source=input.source, name=input.name, author=input.author, link='NULL', doc_type="private")
    return result


from sqlalchemy.types import TypeDecorator, Float
from sqlalchemy.dialects.postgresql import ARRAY

class Vector(TypeDecorator):
    impl = ARRAY(Float)

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value

def query(texts, name, author, source):
    contextualized_texts = [f" {name}, {author}, {source}, {text}" for text in texts]
    response = requests.post(api_url, headers=headers, json={"inputs": contextualized_texts, "options":{"wait_for_model":True}})
    return response.json()

def insertChunksWithLlamaParse(text, source, name='NULL', author='NULL', link='NULL', doc_type="private"):
    chunks = create_chunks(text)

    try:
        with db.engine.begin() as connection:
            result = connection.execute(sqlalchemy.text(
                "INSERT INTO documents2 (name, source, author, link, num_chunks, doc_type) "
                "VALUES (:name, :source, :author, :link, :numchunks, :doc_type) RETURNING id;"
            ), {
                "name": name,
                "source": source,
                "author": author,
                "link": link,
                "numchunks": len(chunks),
                "doc_type": doc_type
            })
            docId = result.scalar_one()

            print(f"Document ID: {docId}")
            print(f"Number of chunks: {len(chunks)}")
            
            # Generate embeddings using contextualized text
            embeddings = query(chunks, name, author, source)
            
            # Insert chunks and their embeddings into the chunks2 table
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                connection.execute(sqlalchemy.text(
                    "INSERT INTO chunks2 (document_id, chunk_index, content, embedding) "
                    "VALUES (:document_id, :chunk_index, :content, :embedding);"
                ), {
                    "document_id": docId,
                    "chunk_index": i,
                    "content": chunk,  # Store only the original chunk text
                    "embedding": json.dumps(embedding)  # Convert embedding list to JSON string
                })

        print("All chunks and embeddings inserted successfully")
        return {"message": f"Document parsed and {len(chunks)} chunks with embeddings saved to database", "document_id": docId}

    except DBAPIError as error:
        print(f"Database error: {error}")
        return {"error": "Database error occurred", "details": str(error)}
    except Exception as e:
        print(f"Error processing document: {e}")
        return {"error": "Error processing document", "details": str(e)}
    
    
    
    
@router.post("/multiple-PDFs")
async def update_multiple_pdfs(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            results.append({"file": file.filename, "status": "error", "message": "Invalid file format. Please upload a PDF file."})
            continue

        try:
            # Use the filename (without extension) as the document name
            name = os.path.splitext(file.filename)[0]
            
            contents = await file.read()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(contents)
                temp_file_path = temp_file.name
            
            file_extractor = {".pdf": parser}
            documents = SimpleDirectoryReader(input_files=[temp_file_path], file_extractor=file_extractor).load_data()
            
            os.unlink(temp_file_path)
            
            if not documents:
                raise ValueError("No content extracted from PDF")
            
            text = "\n".join([doc.text for doc in documents])
            
            # Use the filename as name, set author to "MX GVMT", and use the original filename as the link
            result = insertChunksWithLlamaParse(text=text, name=name, author="MX GVMT", link=file.filename, source="PDF")
            results.append({"file": file.filename, "status": "success", "result": result})
        except Exception as e:
            results.append({"file": file.filename, "status": "error", "message": str(e)})

    return results
