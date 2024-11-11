import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains.llm_math.base import LLMMathChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

## Setup API Streamlit app
st.set_page_config("Text to Math Problem Solver and Data search Asistant", page_icon="💢")
st.title("Text to amth problem Solver with Gamma2")

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")
