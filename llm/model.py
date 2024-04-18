import streamlit as st
import os
import re
from langchain_community.embeddings import HuggingFaceEmbeddings,OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain.chains import RetrievalQA,create_retrieval_chain
from langchain import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.embeddings.openai import OpenAIEmbeddings


class Model:
    
    def __init__(self):
        # Set the Hugging Face API key
        os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"
        self.preprocesspdf()
        
    def preprocesspdf(self):
        embeddings = HuggingFaceEmbeddings()
        print('embedding done')
        persist_directory = 'db'
        
        vectordb = Chroma(persist_directory=persist_directory, 
                    embedding_function=embeddings)
        llm = HuggingFaceHub(repo_id='mistralai/Mistral-7B-Instruct-v0.2',model_kwargs={'temperature':0.1,'max_new_tokens':1000})
        
        prompt = ChatPromptTemplate.from_template("""
        Answer the user's question as a veterinary doctor specialized in cattle by using the context:
        Context: {context}
        Question: {input}""")
        
        chain = create_stuff_documents_chain(llm=llm,prompt=prompt)
        retriever = vectordb.as_retriever()
        global retreival_chain
        retreival_chain = create_retrieval_chain(
            retriever,
            chain
        )
        return 'PDF process successfull'
    def run_retrieval(self, query):
        print("document retreiving")
        response = retreival_chain.invoke({
            "input": query,
        })
        text = dict(response)
        print(text)
        pattern = re.compile(r'Question: (.+?)[?.]\s*(.*)', re.DOTALL)
        # Extracting wordings after "Question" key
        extracted_wordings = []
        for key, value in text.items():
            if isinstance(value, str):  # Checking if value is a string
                match = pattern.search(value)
            if match:
                extracted_wordings.append(match.group(2))
            
        return extracted_wordings[0]
        

