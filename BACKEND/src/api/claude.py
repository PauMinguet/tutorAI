import os
from dotenv import load_dotenv
import requests
from fastapi import APIRouter, Depends
from src.api import searchVectorDB
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

@router.get("/{query}")
def query(query):

    print(query)

    context = searchVectorDB.searchVectorDB(query)

    # Ollama API request
    ollama_url = "http://localhost:11434/api/generate"
    ollama_payload = {
        "model": "claude",  # Assuming you have a Claude model in Ollama
        "prompt": f"System: You are a private AI for a law company, and your goal is to use the sources provided (pieces of textbook, slides, youtube video transcripts, etc), to answer the question best. Feel free to quote them and cite them by their author or name, and, if necessary, refer the lawyer to the source for additional information.\n\nHuman: Answer this query: ({query}) with the following context: {context}\n\nAssistant:",
        "stream": False
    }

    response = requests.post(ollama_url, json=ollama_payload)
    
    if response.status_code == 200:
        answer = response.json()['response']
    else:
        answer = f"Error: Unable to get response from Ollama. Status code: {response.status_code}"

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("insert into queries (query, context, answer) values (:query, :context, :answer);")
            , {"query": query, "context": context, "answer": answer})

    return answer