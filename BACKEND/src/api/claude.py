import os
from dotenv import load_dotenv
import anthropic
from fastapi import APIRouter, HTTPException
from src.api import searchVectorDB
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

# Load environment variables
load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@router.get("/{query}")
def query(query: str):
    print(query)

    context = searchVectorDB.searchVectorDB(query)

    system_prompt = """Eres una IA privada para una empresa de abogados, y tu objetivo es utilizar las fuentes proporcionadas (fragmentos de libros de texto, diapositivas, transcripciones de videos de YouTube, etc.) para responder la pregunta de la mejor manera posible. Siéntete libre de citarlas y mencionar a sus autores o nombres, y, si es necesario, remite al abogado a la fuente para obtener información adicional."""

    try:
        response = client.messages.create(
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
        )
        answer = response.content[0].text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Anthropic API: {str(e)}")

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("insert into queries (query, context, answer) values (:query, :context, :answer);"),
                           {"query": query, "context": context, "answer": answer})

    return answer