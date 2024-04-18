import streamlit as st
from model import Model

st.title("Ask UVA")

    # Creating an instance of the Model
model = Model()

    # Query input
print("query box")
query = st.text_input("Enter your query:")

if st.button("Search"):
    with st.spinner("Searching..."):
            result =  model.run_retrieval(query)
            st.write(result)

