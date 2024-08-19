import json
import os
from fastapi import APIRouter, HTTPException
import sqlalchemy
from src import database as db
from sqlalchemy.exc import DBAPIError

router = APIRouter(
    prefix="/viewDocuments",
    tags=["viewDocuments"],
)

@router.get("/")
def searchVectorDB():
    try:
        with db.engine.begin() as connection:
            query = sqlalchemy.text("""
                SELECT id, name, source, author, link 
                FROM documents 
            """)
            results = connection.execute(query).fetchall()

        if results is None or len(results) == 0:
            print("No results found in the database.")
            return {"results": []}

        formatted_results = [
            {
                "id": result[0],
                "name": result[1],
                "source": result[2],
                "author": result[3],
                "link": result[4]
            }
            for result in results
        ]

        print(f"Number of documents found: {len(formatted_results)}")
        return {"results": formatted_results}

    except DBAPIError as error:
        error_message = f"Database error occurred: {str(error)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)