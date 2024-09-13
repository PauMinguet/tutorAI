import json
import os
from fastapi import APIRouter, Depends
import sqlalchemy
from src import database as db
from sqlalchemy.exc import DBAPIError
import requests

router = APIRouter(
    prefix="/searchVectorDB",
    tags=["searchVectorDB"],
)

model_id = "intfloat/multilingual-e5-small"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}

def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()

@router.get("/{text}")
def searchVectorDB(text):
    print(text)
    
    embedding = query([text])[0]
    
    # Convert the embedding list to a PostgreSQL array string
    embedding_str = f"'[{','.join(map(str, embedding))}]'"
    
    try:
        with db.engine.begin() as connection:
            results = connection.execute(sqlalchemy.text(f"""
    SELECT c.content, d.source, d.name, d.author, d.link
    FROM chunks2 c
    JOIN documents2 d ON c.document_id = d.id
    ORDER BY c.embedding <-> {embedding_str}::vector
    LIMIT 10;
""")).fetchall()
        
        formatted_text = ""
        for result in results:
            if result[3] is not None:
                formatted_text += f"Autor: {result[3]},\n"
            if result[2] is not None:
                formatted_text += f"Nombre: {result[2]},\n"
            if result[1] is not None:
                formatted_text += f"Tipo de Fuente: {result[1]},\n"
            if result[0] is not None:
                formatted_text += f"Texto: {result[0]}\n"
            formatted_text += "\n"

        print(formatted_text)
        return formatted_text
    
    except DBAPIError as error:
        print(f"Error returned: <<<{error}>>>")
        return {"error": str(error)}