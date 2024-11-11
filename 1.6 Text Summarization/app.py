import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader


## Streamlit App
st.set_page_config(page_title= "Summarize the text from any website.", page_icon="🦜")
st.title("🦜 Langchain: Summarize text from any website.")
st.subheader("Summarize URL")


## Get the Groq API key and url to be summarized.
with st.sidebar:
    groq_api_key = st.text_input("Groq API KEY", value= "", type="password")
generic_url = st.text_input("URL", label_visibility="collapsed")


## Gamma Model using Groq Api key
llm= ChatGroq(groq_api_key= groq_api_key, model= "Gemma-7b-It")

