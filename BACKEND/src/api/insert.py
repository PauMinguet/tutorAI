import os
import unicodedata
import PyPDF2
from fastapi import APIRouter, File, UploadFile, Form
from typing import List

#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
import requests
import re
import youtube_transcript_api
from io import BytesIO

#from docx import Document

router = APIRouter(
    prefix="/insert",
    tags=["insert"],
    #dependencies=[Depends(auth.get_api_key)],
)



model_id = "intfloat/multilingual-e5-small"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}

def query(texts, name, author, source):
        for i in range(len(texts)):
            texts[i] = f" {name}, {author}, {source}, {texts[i]}"
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()




class Input(BaseModel):
    link: str
    source: str

@router.post("/YT")
def update_times(input: Input):

    example_url = input.link
    _id = example_url.split("=")[1].split("&")[0]

    channel_pattern = r'channel=([\w\-]+)'
    
    # Search for the pattern in the URL
    channel_match = re.search(channel_pattern, example_url)

    if channel_match:
        channel = channel_match.group(1)
    else:
        channel = None

    title = get_video_title(example_url)


    transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(_id)

    text = ""

    for line in transcript:
        text += line['text'] + " "
    print(len(text))
    
    print(text)
    
    print(input.source)

    insertChunks(text, author=channel, name=title, link=example_url, source=input.source)

    return "YouTube video transcript parsed and saved to database"


class InputFile(BaseModel):
    filename: str
    startpage: int
    endpage: int
    name: str


class InputFile(BaseModel):
    filename: str
    startpage: int
    endpage: int
    name: str

@router.post("/PDF")
def update_times(input: InputFile):
    filename = input.filename
    startpage = input.startpage
    endpage = input.endpage
    name = input.name

    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate to the project root (assuming the current file is in src/api)
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    
    # Construct the path to the assets folder
    assets_dir = os.path.join(project_root, 'assets')
    
    # Full path to the PDF file
    filepath = os.path.join(assets_dir, filename)

    print(f"Attempting to open file: {filepath}")

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"File not found: {filepath}")

    if not filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF file.")

    try:
        with open(filepath, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
            text = ''
            endpage = min(int(endpage), num_pages)
            for page_num in range(int(startpage), endpage):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

    # Call your insertChunks function here
    insertChunks(text=text, name=name, link=filename, source="PDF")

    return {"message": "PDF parsed and saved to database"}



class InputText(BaseModel):
    name: str
    text: str
    source: str
    author: str = 'NULL'



@router.post("/text")
def update_times(input: InputText):
    name = input.name
    text = input.text
    source = input.source
    author = input.author
    
    insertChunks(text, source=source, name=name, author=author, link='NULL')

    return "Document parsed and saved to database"


@router.post("/multiple_pdfs")
async def upload_multiple_pdfs(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            results.append({"filename": file.filename, "status": "error", "message": "Not a PDF file"})
            continue

        try:
            content = await file.read()
            pdf_file = BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            name = os.path.splitext(file.filename)[0]  # Remove .pdf extension
            source = "PLD"
            author = "MX GVMT"

            insertChunks(text=text, name=name, source=source, author=author, link=file.filename)
            
            results.append({"filename": file.filename, "status": "success", "message": "PDF processed and saved to database"})
        except Exception as e:
            results.append({"filename": file.filename, "status": "error", "message": str(e)})

    return results





def insertChunks(text, source, name='NULL', author='NULL', link='NULL'):

    chunks = break_into_chunks(text)

    chunks = [chunk for chunk in chunks if len(chunk) > 100]
    
    chunks = filter_chunks(chunks)

    try:
        with db.engine.begin() as connection:
            docId = connection.execute(sqlalchemy.text("insert into documents (name, source, author, link, num_chunks) values (:name, :source, :author, :link, :numchunks) returning id;")
                , {"text": text, "source": source, "name": name, "author": author, "link": link, "numchunks": len(chunks)}).first()[0]
    except DBAPIError as error:
        
        print(f"Error returned: <<<{error}>>>")
        
    print("docId: ", docId)
    print("Number of chunks: ", len(chunks))
                
    print("Inserting chunks:")
    for i in range(0, len(chunks), 100):

        chunks = chunks[i:i+100]
        print(str(i) + " - " + str(i+100))

        embeddings = query(chunks, name, author, source)
        
        try:
            with db.engine.begin() as connection:
                for text, embedding in zip(chunks, embeddings):  
                    if text != '':
                        connection.execute(sqlalchemy.text("insert into items (text_value, embedding, doc_id) values (:text, :embedding, :docId);")
                , {"text": text, "embedding": embedding, "docId": docId})
        
            return "Ok"
        
        except DBAPIError as error:
        
            print(f"Error returned: <<<{error}>>>")


def filter_chunks(chunks, min_avg_word_length=4, max_avg_word_length=8):
    filtered_chunks = []
    
    for chunk in chunks:
        # Split the chunk into words
        words = chunk.split()
        
        # Calculate the average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Check if the average word length is within the allowed range
        if min_avg_word_length <= avg_word_length <= max_avg_word_length:
            filtered_chunks.append(chunk)
    
    return filtered_chunks



def get_video_title(video_url):
    # try:
    #     yt = YouTube(video_url)
    #     return yt.title
    # except Exception as e:
    #     print("Error:", e)
        return None
    

def break_into_chunks(text, max_words=200, overlap=30):

    words = re.findall(r'\w+', text)
    chunks = []
    current_chunk = []
    
    for i, word in enumerate(words):
        if len(current_chunk) + 1 > max_words:
            chunks.append(' '.join(current_chunk[:-overlap]))
            current_chunk = current_chunk[-overlap:]
        
        current_chunk.append(word)
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    chunks = [chunk for chunk in chunks if len(chunk) > 80]
    return chunks


def preprocess_book(text):

    # Remove header/footer patterns
    text = re.sub(r'(?m)^\(c\) \w+\s\d{4}.*?$', '', text)  # Remove copyright lines
    text = re.sub(r'(?m)^Chapter \d+\s*$', '', text)  # Remove chapter headers
    
    # Remove page numbers
    text = re.sub(r'(?m)^\d+\s*$', '', text)  # Remove line numbers
    
    # Normalize text (optional)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Split into input units (e.g., paragraphs)
    paragraphs = re.split(r'\n\n+', text)
    
    preprocessed_inputs = []
    for paragraph in paragraphs:
        if len(paragraph) > 0:
            preprocessed_inputs.append(paragraph)
    
    return preprocessed_inputs