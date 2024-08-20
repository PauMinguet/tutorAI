from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import searchVectorDB, insert, claude, viewDocuments, classes, users
from src.api import ocr
import logging
from .. import database as db
import sqlalchemy
import json

from fastapi.middleware.cors import CORSMiddleware


origins = ["http://localhost:3000"]  # Replace with the URL of your Next.js app


description = """
___
"""

app = FastAPI(
    title="__",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Pau Minguet",
        "email": "pminguet@calpoly.edu",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(users.router)
app.include_router(insert.router)
app.include_router(searchVectorDB.router)
app.include_router(claude.router)
app.include_router(viewDocuments.router)
app.include_router(classes.router)
app.include_router(ocr.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    with db.engine.begin() as connection:
        row = connection.execute(sqlalchemy.text("SELECT * FROM users")).first()
        print(row[2])
    return row[2]










