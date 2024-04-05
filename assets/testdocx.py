from docx import Document
import os

# Read the content of a DOCX file
current_path = os.getcwd()
filepath = current_path + "/assets/321.docx"

# Extract text from a DOCX file
text = textract.process(filepath)

# Decode the extracted text (it's in bytes by default)
text = text.decode('utf-8')

# Print the extracted text
print(text.encode('utf-8', errors='replace').decode('utf-8'))