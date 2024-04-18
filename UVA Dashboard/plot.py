import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px

# MongoDB connection details
URI = "mongodb+srv://unisysveterinaryassistant:VAYbcqWTXJoWPBIn@cluster0.bni0uww.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Animaldisease"
COLLECTION_NAME = "Animaldetails"

def connect():
    client = pymongo.MongoClient(URI)
    db = client[DB_NAME]
    global collection
    collection = db[COLLECTION_NAME]
    # Retrieve data from MongoDB
    data = collection.find()
    global df
    # Convert data to DataFrame
    df = pd.DataFrame(list(data))

    # Convert ObjectId to string for _id field
    df['_id'] = df['_id'].astype(str)

    # Convert date field to datetime
    df['date'] = pd.to_datetime(df['date'])
    


def dashboard_section():
    connect()
    st.markdown("<h1 style='text-align: left; color: #49f222; font-size: 46px; font-weight:600;'>Dashboard</h1>", unsafe_allow_html=True)
    # Create a bar chart for each disease count
    st.subheader('Chart of Disease Counts')
    fig_bar = px.bar(df, x='date', y=['lumpy_skin_count', 'mouth_disease_count'],
                    title='Counts of Different Diseases',
                    labels={'value': 'Count', 'date': 'Date of affect', 'variable': 'Disease'},
                    color_discrete_map={'lumpy_skin_count': '#85cf58', 'mouth_disease_count': '#548338'})
    st.plotly_chart(fig_bar)
    st.set_option('deprecation.showPyplotGlobalUse', False) 

    # Create a horizontal line chart for disease counts over time
    st.subheader('Horizontal Line Chart of Disease Counts Over Time')
    fig_line_horizontal = px.line(df, x=['lumpy_skin_count', 'mouth_disease_count'], y='date',
                                title='Trend of Disease Counts Over Time',
                                labels={'value': 'Count', 'date': 'Date', 'variable': 'Disease'},
                                color_discrete_map={'lumpy_skin_count': '#85cf58', 'mouth_disease_count': '#19883f'},
                                orientation='h')
    st.plotly_chart(fig_line_horizontal)

    
