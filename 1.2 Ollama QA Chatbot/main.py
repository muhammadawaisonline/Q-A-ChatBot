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

