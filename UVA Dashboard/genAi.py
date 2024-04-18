import streamlit as st
import google.generativeai as genai

genai.configure(api_key='AIzaSyDPDemtvtVtmXj9BKcljiSm-l8fFbGjHOA')
model = genai.GenerativeModel('gemini-pro')

def genai_section():
    st.markdown("<h1 style='text-align: left; color: #49f222; font-size: 46px; font-weight:600;'>UVA\'s AI</h1>", unsafe_allow_html=True)
    # Add a text input widget for user input
    prompt = st.text_input('Enter your prompt:')
    
    # Add a button to trigger content generation
    if st.button('Generate Content'):
        if prompt:
            animal_prompt = f"{prompt} give relating to agriculture "
            optresponse = generate_content(animal_prompt)
            st.markdown(optresponse)
        else:
            st.warning('Please enter a prompt.')
            
def generate_content(prompt):
    try:
        response = model.generate_content(prompt)
        optresponse = response._result.candidates[0].content.parts[0].text
        return optresponse
    except Exception as e:
        return f"Error generating content: {e}"
    
    