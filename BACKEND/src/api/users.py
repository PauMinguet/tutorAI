import os
import unicodedata
from fastapi import APIRouter, Depends
#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
import requests
import re
import youtube_transcript_api
from pytube import YouTube
#from docx import Document

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

class User(BaseModel):
    firstname: str
    lastname: str
    email: str
    userid: str

@router.post("/create")
def update_times(user: User):
    firstname = user.firstname
    lastname = user.lastname
    email = user.email
    userid = user.userid

    try:
        with db.engine.begin() as connection:
            userId = connection.execute(sqlalchemy.text(f"""
INSERT INTO users (firstname, lastname, email, userid) VALUES ('{firstname}', '{lastname}', '{email}', '{userid}');
"""))
        
        

        return "User created successfully!"
    
    except DBAPIError as error:
     
        print(f"Error returned: <<<{error}>>>")
    