import os
import anthropic
from dotenv import load_dotenv
import requests
from fastapi import APIRouter, Depends
from src.api import searchVectorDB
from src import database as db
import sqlalchemy

#from src.api import auth

router = APIRouter(
    prefix="/query",
    tags=["query"],
    #dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{query}")
def query(query):
    load_dotenv()

    print(query)

    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
        
    )
    context = searchVectorDB.searchVectorDB(query)

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0,
        system="You are a private tutor, called tutorAI, and your goal is to use the sources provided (pieces of textbook, slides, youtube video transcripts, etc), to answer the question best. Feel free to quote them and cite them by their author or name, and, if necessary, refer the student to the source for additional information.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Answer this query: {query} with the following context: {context}"
                    }
                ]
            }
        ]
    )


    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("insert into queries (query, context, answer) values (:query, :context, :answer);")
            , {"query": query, "context": context, "answer": message.content[0].text})

    return message.content[0].text