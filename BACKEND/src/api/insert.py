import os
import unicodedata
import PyPDF2
from fastapi import APIRouter, Depends
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
import requests
import re
import youtube_transcript_api
from pytube import YouTube
#from docx import Document

router = APIRouter(
    prefix="/insert",
    tags=["insert"],
    #dependencies=[Depends(auth.get_api_key)],
)


class Input(BaseModel):
    link: str
    source: str

@router.post("/YT")
def yt(input: Input):

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
    

    chunks = break_into_chunks(text)

    #print(len(chunks))

    #for i in range(len(chunks)):
        #print(len(chunks[i]))

    insertChunks(chunks, author=channel, name=title, link=example_url, source=input.source)

    return "YouTube video transcript parsed and saved to database"


class InputFile(BaseModel):
    filename: str
    startpage: int
    endpage: int
    name: str


@router.post("/PDF")
def pdf(input: InputFile):
    filename = input.filename
    startpage = input.startpage
    endpage = input.endpage
    name = input.name

    current_path = os.getcwd()
    #print(current_path)
    filepath = current_path + f"\\assets\\{filename}"

    filepath = f"/assets/{filename}"


    filepath = filepath.replace("\\", "/")

    if filename.endswith('.pdf'):
        pdf_file = open(filepath, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        text = ''
        endpage = int(endpage) if int(endpage) < num_pages else num_pages
        for page_num in range(int(startpage), endpage):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        pdf_file.close()
    else:
        return "Invalid file format. Please upload a PDF file."

    chunks = break_into_chunks(text)

    print(len(chunks))

    print("Inserting chunks:")
    for i in range(0, len(chunks), 100):

        insertChunks(chunks[i:i+100], source="PDF", name=name, link=filename)
        print(str(i) + " - " + str(i+100))

    return "PDF parsed and saved to database"


class InputDOCX(BaseModel):
    filename: str
    name: str


class InputText(BaseModel):
    name: str
    text: str
    source: str
    author: str = 'NULL'



from fastapi import WebSocket
from typing import Generator


@router.post("/text")
async def text(input: InputText, websocket: WebSocket = Depends(get_websocket)):
    name = input.name
    text = input.text
    source = input.source
    author = input.author
    chunks = break_into_chunks(text)

    await websocket.accept()

    total_chunks = len(chunks)
    inserted_chunks = 0

    async def insert_chunks() -> Generator[int, None, None]:
        nonlocal inserted_chunks
        for i in range(0, len(chunks), 100):
            try:
                insertChunks(chunks[i:i+100], source=source, name=name, author=author, link='NULL')
                inserted_chunks += 100
                yield inserted_chunks
            except Exception as e:
                print(f"Error inserting chunks: {e}")
                yield -1  # Indicate an error

    async for progress in insert_chunks():
        if progress == -1:
            await websocket.send_json({"status": "error", "message": "Error inserting chunks"})
        else:
            await websocket.send_json({"status": "progress", "value": progress, "total": total_chunks})

    await websocket.send_json({"status": "complete", "message": "PDF parsed and saved to database"})
    await websocket.close()

    return {"status": "PDF parsed and saved to database"}








model_id = "intfloat/e5-small-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}

def query(texts):
        response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
        return response.json()


def insertChunks(lst, source, name='NULL', author='NULL', link='NULL'):

    lst = [chunk for chunk in lst if len(chunk) > 100]

    embeddings = query(lst)
    
    try:
        with db.engine.begin() as connection:
            for text, embedding in zip(lst, embeddings):  
                if text != '':
                    connection.execute(sqlalchemy.text("insert into items (text_value, embedding, source, name, author, link) values (:text, :embedding, :source, :name, :author, :link);")
            , {"text": text, "embedding": embedding, "source": source, "name": name, "author": author, "link": link})

        return "Ok"

    except DBAPIError as error:
    
        print(f"Error returned: <<<{error}>>>")







def get_video_title(video_url):
    try:
        yt = YouTube(video_url)
        return yt.title
    except Exception as e:
        print("Error:", e)
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