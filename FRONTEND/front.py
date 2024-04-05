import streamlit as st
import requests
import fileToText
import base64





def main():
    pages = ["Home", "Login", "SignUp"]

    st.sidebar.title("Navigation")
    choice = st.sidebar.selectbox("Menu", pages)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            if password == "12345":  # Dummy password check
                st.success("Logged In as {}".format(username))
                home()

    elif choice == "Login":
        st.subheader("Login Section")
        user = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.sidebar.button("Login"):
            if password == "12345":  # Dummy password check
                st.success("Logged In as {}".format(username))
                home()


    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Signup"):
            st.success("You have successfully created an account")
            st.info("Go to Login Menu to login")








# Define the pages
def landing_page():
    st.title("tutorAI")
    st.write("This is the landing page.")



def upload_page():
    st.title("Upload Page")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        # Read the file
        file_content = uploaded_file.read()

        # Convert the file content to base64
        file_content_base64 = base64.b64encode(file_content).decode()

        # Define the API endpoint
        url = "https://tutorai-k0k2.onrender.com/insert/text"

        # Define the request payload
        payload = {
            "name": "TEST",
            "text": file_content_base64,
            "source": "TEST"
        }

        # Send a POST request to the API
        response = requests.post(url, json=payload)

        # Handle the response
        if response.status_code == 200:
            st.write("API call was successful!")
        else:
            st.write("API call failed.")



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
        output_height = max(100, len(output_text.split('\n')) * 20)

        st.text_area("Output", value=output_text, height=output_height)

def settings_page():
    st.title("Settings Page")
    st.write("This is the settings page.")

def home():
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