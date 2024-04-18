import streamlit as st
from streamlit_option_menu import option_menu
from genAi import genai_section
from Additional import additional_section
from plot import dashboard_section
from symptoms import disease_finder
from location import locate 

# Define function for each page
def home():
    st.markdown("<h1 style='text-align: left; color: #49f222; font-size: 46px; font-weight:600;'>Home</h1>", unsafe_allow_html=True)
    st.write("Welcome to the Home page!")
    
    # Add images
    st.image("image2.jpg", use_column_width=True)
    
    st.write("Monitor your farm with us!")
    st.write("All in one solution for monitoring your farm")


# Main function to run the app
def main():

    # Define icons for each navigation option
    icons = {
        "Home": "",
        "UVA's Ai": "",
        "Data Visualization": "",
        "Analyze": "",
        "Predictor": "",
        "Locate Doctor": "",
    }

    # Create top navigation bar
    with st.sidebar:
        app = option_menu(
            menu_title="",
            options=[
                "🏠 ‎ ‎ Home",
                "💬 ‎ ‎ UVA's Ai",
                "📊 ‎ ‎ Data Visualization",
                "🔍 ‎ ‎ Analyze",
                "📈 ‎ ‎ Predictor",
                "🗺️ ‎ ‎ Locate Doctor",
            ],
            icons=[f"{icon}-fill" for icon in icons.values()],
            menu_icon="",
            default_index=0,
            styles={
                "container": {
                    "padding": "5px !important",
                    "background-color": "#0b2419",
                    "font-family": "Poppins",
                },
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "color": "white",
                    "font-size": "17px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#188957",
                },
                "nav-link-selected": {
                    "background-color": "#0b3e26",
                    "font-family": "Poppins",
                    "font-weight": "500",
                },
            },
        )

    # Display corresponding page based on selection
    if app == "🏠 ‎ ‎ Home":
        home()
    elif app == "💬 ‎ ‎ UVA's Ai":
        genai_section()
    elif app == "📊 ‎ ‎ Data Visualization":
        dashboard_section()
    elif app == "🔍 ‎ ‎ Analyze":
        additional_section()
    elif app == "📈 ‎ ‎ Predictor":
        disease_finder()
    elif app == "🗺️ ‎ ‎ Locate Doctor":
        locate()


if __name__ == "__main__":
    main()