import json
import os
from fastapi import APIRouter, Depends
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
import requests

router = APIRouter(
    prefix="/searchVectorDB",
    tags=["searchVectorDB"],
    #dependencies=[Depends(auth.get_api_key)],
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

        
    try:
        with db.engine.begin() as connection:
            results = connection.execute(sqlalchemy.text(f"""
    SELECT i.text_value, d.source, d.name, d.author, d.link
    FROM itemsw i
    JOIN documents d ON i.doc_id = d.id
    ORDER BY i.embedding <=> '{embedding}'
    LIMIT 20;
""")).fetchall()
        
        formatted_text = ""
        for result in results:
            if result[3] is not None:
                formatted_text += f"Author: {result[3]},\n"
            if result[2] is not None:
                formatted_text += f"Name: {result[2]},\n"
            if result[1] is not None:
                formatted_text += f"Type of Source: {result[1]},\n"
            if result[4] is not None:
                formatted_text += f"Link: {result[4]},\n"
            if result[0] is not None:
                formatted_text += f"Text: {result[0]}\n"

        print(formatted_text)

        return formatted_text
    
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")
    
