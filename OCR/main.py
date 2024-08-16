import easyocr
import fitz  # PyMuPDF
import os
import tempfile
import requests
import json
import re

def extract_and_format_text_from_pdf(pdf_path):
    # Initialize the OCR reader for Spanish
    reader = easyocr.Reader(['es'])  # 'es' for Spanish
    print("OCR reader initialized")

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory: {temp_dir}")

        pdf_document = fitz.open(pdf_path)
        
        if len(pdf_document) == 0:
            print("The PDF file is empty.")
            return ""

        first_page = pdf_document[0]
        pix = first_page.get_pixmap()
        image_path = os.path.join(temp_dir, "page_1.png")
        pix.save(image_path)
        print(f"Saved first page as image: {image_path}")

        pdf_document.close()

        result = reader.readtext(image_path)
        
        extracted_text = ""
        for detection in result:
            extracted_text += detection[1] + "\n"

    # Pre-format the extracted text
    pre_formatted_text = pre_format_text(extracted_text)
    
    # Refine the pre-formatted text using LLaMA
    final_formatted_text = refine_text_with_llama(pre_formatted_text)
    
    return final_formatted_text

def pre_format_text(text):
    # Split text into lines
    lines = text.split('\n')
    
    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]
    
    # Attempt to identify and group related information
    formatted_lines = []
    current_group = []
    
    for line in lines:
        if re.match(r'^[A-Z\s]+:$', line):  # Possible header
            if current_group:
                formatted_lines.append('\n'.join(current_group))
                current_group = []
            current_group.append(line)
        else:
            current_group.append(line)
    
    if current_group:
        formatted_lines.append('\n'.join(current_group))
    
    return '\n\n'.join(formatted_lines)

def refine_text_with_llama(text):
    url = "http://localhost:11434/api/generate"
    
    prompt = f""" Format this information in Spanish in this format (The names will be in this order: Last1, Last2, First):
    
    (titulo)
    
    Nombre Completo:
    Sexo:
    Fecha de Nacimiento:
    Dirección:
    Clave de Elector:
    CURP:
    Sección Electoral:
    Vigencia:
    CNE:
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

# Usage
pdf_path = "pdf.pdf"  # Replace with your PDF file path
formatted_text = extract_and_format_text_from_pdf(pdf_path)
print(formatted_text)