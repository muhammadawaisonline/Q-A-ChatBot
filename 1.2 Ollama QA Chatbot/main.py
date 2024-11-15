import openai
import streamlit as st
from langchain_community.llms import ollama 
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv
load_dotenv()


os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "QA Chatbot"

# defining chat prompt

prompt =  ChatPromptTemplate.from_messages(

    [
        ("system", "You are helpful asistant. Please respond to the queries."),
        ("user", "Question: {question}")

    ]
)

def generate_response(question, engine, temprature, max_tokens):
    llm = ollama(model= engine)
    output_parser = StrOutputParser()
    chain= prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

# Title of the app
st.title("QA ChatBot with OPENAI")

#sidebar for settings

st.sidebar.title("settings")


# Drop down to select AI models
engine = st.sidebar.selectbox("Select an Openai Model", ["llama3.2"])

# adjust response parameter
temprature = st.sidebar.slider("Temprature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

