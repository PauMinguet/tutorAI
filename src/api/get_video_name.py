import requests
from bs4 import BeautifulSoup

# Replace with the actual Quizlet URL
url = "https://quizlet.com/123456789/your-quizlet-set"

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the terms and definitions
terms_and_definitions = soup.find_all("span", class_="TermText")

# Print the terms and definitions
for term_def in terms_and_definitions:
    term_text = term_def.text.split(" is ")[0]
    definition_text = "is " + term_def.text.split(" is ")[1]
    print(f"Term: {term_text}")
    print(f"Definition: {definition_text}")
    print("-" * 20)