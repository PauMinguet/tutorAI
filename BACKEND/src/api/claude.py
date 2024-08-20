import os
from dotenv import load_dotenv
import anthropic
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from src.api import searchVectorDB
from src import database as db
import sqlalchemy
import asyncio

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@router.get("/{query}")
async def query(query: str):
    print(query)

    context = searchVectorDB.searchVectorDB(query)

    system_prompt = """Eres una IA privada para una empresa de abogados, y tu objetivo es utilizar las fuentes proporcionadas (fragmentos de libros de texto, diapositivas, transcripciones de videos de YouTube, etc.) para responder la pregunta de la mejor manera posible. Siéntete libre de citarlas y mencionar a sus autores o nombres, y, si es necesario, remite al abogado a la fuente para obtener información adicional."""

    async def generate():
        try:
            with client.messages.stream(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": f"Responde a esta consulta: ({query}) con el siguiente contexto: {context}"
                    }
                ]
            ) as stream:
                answer = ""
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        content = chunk.delta.text
                        answer += content
                        yield content

            # Store the complete answer in the database
            with db.engine.begin() as connection:
                connection.execute(sqlalchemy.text("insert into queries (query, context, answer) values (:query, :context, :answer);"),
                                   {"query": query, "context": context, "answer": answer})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling Anthropic API: {str(e)}")

    return StreamingResponse(generate(), media_type="text/event-stream")