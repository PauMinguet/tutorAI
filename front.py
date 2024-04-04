import streamlit as st
import requests

# Define the pages
def landing_page():
    st.title("tutorAI")
    st.write("This is the landing page.")

def upload_page():
    st.title("Upload Page")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        # You can add additional code here to process the uploaded file

def query_page():
    st.title("Query Page")

    # Input text box
    input_text = st.text_input("Enter some text:")

    # Send button
    if st.button("Send"):
        try:
            # Make an API call
            api_url = f"http://127.0.0.1:3000/query/{input_text}"
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
        st.text_area("Output", value=output_text, height=600)

def settings_page():
    st.title("Settings Page")
    st.write("This is the settings page.")

def main():
    # Set up the navigation menu
    pages = {
        "Landing": landing_page,
        "Upload": upload_page,
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