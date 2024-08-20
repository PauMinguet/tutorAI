import os
import unicodedata
import PyPDF2
from fastapi import APIRouter, File, UploadFile, Form
import tempfile
from typing import List

#from src.api import auth
import sqlalchemy
from src import database as db
from operator import itemgetter
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel
import requests
import re
import youtube_transcript_api
from io import BytesIO
import easyocr
import pymupdf as fitz


#from docx import Document

router = APIRouter(
    prefix="/ocr",
    tags=["ocr"],
)

@router.post("")
async def ocr(file: UploadFile = File(...)):
    # Create a temporary file to store the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        # Write the uploaded file content to the temporary file
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Process the PDF file using the imported function
        formatted_text = extract_and_format_text_from_pdf(temp_file_path)
        
        # Return the formatted text
        return {"formatted_text": formatted_text}
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        
        

def extract_and_format_text_from_pdf(pdf_path):
    # Initialize the OCR reader for Spanish
    reader = easyocr.Reader(['es'])  # 'es' for Spanish
    #print("OCR reader initialized")

    with tempfile.TemporaryDirectory() as temp_dir:
        #print(f"Created temporary directory: {temp_dir}")

        pdf_document = fitz.open(pdf_path)
        
        if len(pdf_document) == 0:
            print("The PDF file is empty.")
            return ""

        first_page = pdf_document[0]
        pix = first_page.get_pixmap()
        image_path = os.path.join(temp_dir, "page_1.png")
        pix.save(image_path)
        #print(f"Saved first page as image: {image_path}")

        pdf_document.close()

        result = reader.readtext(image_path)
        
        extracted_text = ""
        for detection in result:
            extracted_text += detection[1] + "\n"

    # Pre-format the extracted text
    
    # Refine the pre-formatted text using LLaMA
    formatted_text = refine_text_with_llama(extracted_text)
    
    return formatted_text


def refine_text_with_llama(text):
    url = "http://localhost:11434/api/generate"
    
    prompt = f"""Formatea esta información en español en el siguiente formato:
- Los nombres estarán en este orden: Apellido1, Apellido2, Nombre. Asegurate de que los nombres y apellidos estén separados por una coma.:
- La fecha de nacimiento estará en el formato DD/MM/AAAA:
- Adhiérete al siguiente formato, no omitas ningun campo:
        
    Nombre Completo:
    Sexo:
    Fecha de Nacimiento:
    Domicilio:
    Clave de Elector:
    CURP:
    Sección Electoral:
    Año de Registro:
    Vigencia:
    IDMEX:
        
    {text}
    """
    
    print(prompt)

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['response']
    except requests.exceptions.RequestException as e:
        print(f"Error al comunicarse con el modelo LLaMA: {e}")
        return text  # Return pre-formatted text if LLaMA processing fails
