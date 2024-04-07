import io
import pandas as pd
import PyPDF2
import streamlit as st
import requests

# Add a new state variable to keep track of the current page

def main():
    home()

# Define the pages
def landing_page():
    st.title("tutorAI")
    st.write("Welcome to tutorAI! This is a tool that helps you generate answers to queries using the sources provided. You can upload a PDF, enter a query, and get a personalized answer generated by tutorAI. It works best with school materials, such as textbooks, slideshows, and research papers. Give it a try and see how it can help you with your studies!")
    st.write("Lots more features coming soon!")

def upload_pdf_page():
    st.title("Upload PDF")

    # Add text inputs for Name and Author
    name = st.text_input("Name")
    author = st.text_input("Author")

    # Add a dropdown for Source
    source_options = ["Textbook", "Book", "Slideshow", "Journal Article", "Research Paper", "Other"]
    source = st.selectbox("Resource", source_options)
    
    startpage = int(st.text_input("Start Page", '0'))
    endpage = int(st.text_input("End Page", '10000000'))

    uploaded_file = st.file_uploader("Choose a file", accept_multiple_files=False)

    if st.button("Upload"):
            
            # Check if the uploaded file is a PDF
        if uploaded_file.name.endswith('.pdf'):
            st.write("File uploaded successfully!")

            # Read the file
            pdf_file = uploaded_file.read()
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            num_pages = len(pdf_reader.pages)
            text = ''

            # Extract text from the PDF
            for page_num in range(startpage, endpage if endpage < num_pages else num_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            print(text)

            url = "https://tutorai-k0k2.onrender.com/insert/text"

            # Define the request payload
            payload = {
                "name": name,
                "text": text,
                "source": source,
                "author": author
            }

            # Send a POST request to the API
            response = requests.post(url, json=payload)

                # Handle the response
            if response.status_code == 200:
                st.write("Inserted successfully!")
            else:
                st.write("Something went wrong :( Please try again.")
        else:
            st.write("Invalid file format. Please upload a PDF file.")
            

def query_page():
    st.title("Query Page")

    # Input text box
    input_height = 100
    input_text = st.text_area("Enter some text:", height=input_height)
    input_height = max(100, len(input_text.split('\n')) * 20)

    # Send button
    if st.button("Send"):
        try:
            
            # Make an API call
            api_url = f"https://tutorai-k0k2.onrender.com/query/{input_text}"
            print(api_url)
            #payload = {"query": input_text}
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for non-2xx status codes

            # Process the API response
            data = response.json()
            output_text = data
        except requests.exceptions.RequestException as e:
            output_text = f"Error: {e}"

        # Output text box

        st.text_area("Output", value=output_text, height=800)

def upload_youtube_page():
    st.title("Upload YouTube Video")
    st.write("This is the YouTube upload page.")
    
    link = st.text_input("YouTube Video Link")

    # Add a dropdown for Source
    source_options = ["Lecture", "YouTube Video", "AudioBook", "Presentation", "Other"]
    source = st.selectbox("Type", source_options)
    

    if st.button("Upload"):
        
        # Check if the uploaded file is a PDF
        
        url = "https://tutorai-k0k2.onrender.com/insert/YT"

            # Define the request payload
        payload = {
            "source": source,
            "link": link
        }

            # Send a POST request to the API
        response = requests.post(url, json=payload)

                # Handle the response
        if response.status_code == 200:
            st.write("Inserted successfully!")
        else:
            st.write("Something went wrong :( Please try again.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def upload_text_page():
    st.title("Upload Text")
    st.write("This is the text upload page.")
    
    # Add text inputs for Name and Author
    name = st.text_input("Name")
    author = st.text_input("Author")

    # Add a dropdown for Source
    source_options = ["Zoom Transcript", "Textbook", "Book", "Slideshow", "Journal Article", "Research Paper", "Other"]
    source = st.selectbox("Resource", source_options)
    
    input_height = 300
    input_text = st.text_area("Enter some text:", height=input_height)


    if st.button("Upload"):
        
        # Check if the uploaded file is a PDF
        
        url = "https://tutorai-k0k2.onrender.com/insert/text"

            # Define the request payload
        payload = {
            "name": name,
            "text": input_text,
            "source": source,
            "author": author
        }

            # Send a POST request to the API
        response = requests.post(url, json=payload)

                # Handle the response
        if response.status_code == 200:
            st.write("Inserted successfully!")
        else:
            st.write("Something went wrong :( Please try again.")
    
def view_documents_page():
    st.title("View Documents")
    st.write("This is the view documents page.")
    
    url = "https://tutorai-k0k2.onrender.com/viewDocuments"

    response = requests.get(url)
    data = response.json()

    # Display each row as a separate column layout with a delete button
    for i, result in enumerate(data["results"]):
        col1, col2 = st.beta_columns([4, 1])
        with col1:
            st.text(f"Name: {result['name']}")
            st.text(f"Source: {result['source']}")
            st.text(f"Author: {result['author']}")
            st.text(f"Link: {result['link']}")
        with col2:
            if st.button(f"Delete {i}"):
                st.write(f"You clicked delete for item {i}")
                # Add your deletion logic here
    

def settings_page():
    st.title("Settings Page")
    st.write("This is the settings page.")


def home():
    # Set up the navigation menu
    pages = {
        "Landing": landing_page,
        "Upload PDF": upload_pdf_page,
        "Upload YouTube Video": upload_youtube_page,
        "Upload Text": upload_text_page,
        "View Documents": view_documents_page,
        "Query": query_page,
        "Settings": settings_page,
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Set the width of the sidebar using CSS
    st.markdown(
        """
        <style>
        [data-baseweb="sidebar"] {
            width: 200px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display the selected page
    pages[selection]()

if __name__ == "__main__":
    main()