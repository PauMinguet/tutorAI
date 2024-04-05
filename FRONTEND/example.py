import streamlit as st

# Define the pages
def home_page():
    st.title("Home Page")
    st.write("This is the home page.")

def about_page():
    st.title("About Page")
    st.write("This is the about page.")

def contact_page():
    st.title("Contact Page")
    st.write("This is the contact page.")

# Define the function to handle page navigation
def navigate_to(page_name):
    st.session_state.current_page = page_name

# Set the initial page in the session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Main function
def main():
    # Display the navigation buttons in the sidebar
    st.sidebar.title("Navigation")

    with st.sidebar:
        st.write("---")
        if st.button("Home", key="home_button"):
            navigate_to("home")
        st.write("---")
        if st.button("About", key="about_button"):
            navigate_to("about")
        st.write("---")
        if st.button("Contact", key="contact_button"):
            navigate_to("contact")
        st.write("---")

    # Display the selected page
    pages = {
        "home": home_page,
        "about": about_page,
        "contact": contact_page,
    }
    pages[st.session_state.current_page]()

if __name__ == "__main__":
    main()