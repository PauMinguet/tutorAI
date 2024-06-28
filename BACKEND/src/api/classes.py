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
    userId: str

@router.post("/create")
def createClass(input: Input):
    name = input.name
    userid = input.userId
    
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text("""insert into classes (name, user_id) values (:name, :userid)"""), {"name": name, "userid": userid})
        
        return 'Class created!'
    
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")
    

class InputAdd(BaseModel):
    docId: int
    classId: int
    userId: str

@router.post("/add")
def addDocToClass(input: InputAdd):
    docId = str(input.docId)
    classId = str(input.classId)
    userId = input.userId
    
    try:
        with db.engine.begin() as connection:
            connection.execute(sqlalchemy.text("""insert into doctoclass (doc_id, class_id, user_id) values (:docId, :classId, :userId)"""), {"docId": docId, "classId": classId, "userId": userId})
        
        return 'Document added to Class!'
    
    except DBAPIError as error:
    
        print(f"Error returned: <<<{error}>>>")
    

