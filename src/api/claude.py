import os
import anthropic
from dotenv import load_dotenv
import requests
from fastapi import APIRouter, Depends
from src.api import searchVectorDB
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

    print(context)


    with client.messages.stream(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0,
        system="You are a private tutor, called tutorAI, and your goal is to use the sources provided (pieces of textbook, slides, youtube video transcripts, etc), to answer the question best. Feel free to quote them and cite them, and, if necessary, refer the student to the source for additional information.",
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
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print("RESPONSE:")
    print(text)
    return stream.text_stream