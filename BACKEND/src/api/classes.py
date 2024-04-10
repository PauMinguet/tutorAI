from dotenv import load_dotenv
from pydantic import BaseModel
import requests
from fastapi import APIRouter, Depends
from sqlalchemy.exc import DBAPIError
from src import database as db
import sqlalchemy

#from src.api import auth

router = APIRouter(
    prefix="/classes",
    tags=["classes"],
    #dependencies=[Depends(auth.get_api_key)],
)


class Input(BaseModel):
    name: str

@router.post("/create")
def createClass(input: Input):
    name = input.name
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text("""insert into classes (name) values (:name)"""), {"name": name})
        
        return 'Class created!'
    
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")
    

class InputAdd(BaseModel):
    docId: int
    classId: int

@router.post("/add")
def addDocToClass(input: InputAdd):
    docId = str(input.docId)
    classId = str(input.classId)
    
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text("""insert into docToClass (docId, classId) values (:docId, :classId)"""), {"docId": docId, "classId": classId})
        
        return 'Document added to Class!'
    
    except DBAPIError as error:
    
        print(f"Error returned: <<<{error}>>>")
    

