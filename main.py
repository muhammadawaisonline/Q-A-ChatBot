import openai
import streamlit as st
from langchain_openai import ChatOpenAI
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
        ("system", "You are helpful asistant. Please respond to the quereis."),
        ("user", "Question: {question}")

    ]
)

def generate_response(question, api_key, llm, temprature, max_tokens):
    openai.api_key= api_key
    llm = ChatOpenAI(model=llm)
    output_parser = StrOutputParser()
    chain= prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer

# Title of the app
st.title("QA ChatBot with OPENAI")

#sidebar for settings

st.sidebar.title("settings")
api_key = st.sidebar.text_input("Enter your Open API key", type="password")

# Drop down to select AI models
llm = st.sidebar.selectbox("Select an Openai Model", ["gpt-4", "gpt-4o", "gpt-4-turbo"])

# adjust response parameter
temprature = st.sidebar.slider("Temprature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

#main interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You: ")
if user_input and api_key:
    response = generate_response(user_input, api_key=api_key, llm=llm, temprature=temprature, max_tokens=max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter open api key in the sidbar")
else:
    st.warning("Please provide the user input")
    






