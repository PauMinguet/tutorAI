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
    prefix="/viewDocuments",
    tags=["viewDocuments"],
    #dependencies=[Depends(auth.get_api_key)],
)


@router.get("/")
def searchVectorDB():

    
    try:
        with db.engine.begin() as connection:
            results = connection.execute(sqlalchemy.text("""select id, name, source, author, link from documents order by created_at desc""")).fetchall()

        results = [dict(zip(["id", "name", "source", "author", "link"], result)) for result in results]

        
        return {"results": results}
    
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")
    

