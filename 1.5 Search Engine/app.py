import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, agent_types
from langchain.callbacks import StreamlitCallbackHandler

import os 
from dotenv import load_dotenv
load_dotenv()



arxive_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=250)
arxive = ArxivQueryRun(api_wrapper=arxive_wrapper)
wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=250)
wikipedia = WikipediaQueryRun(api_wrapper=wiki_wrapper)
search =  DuckDuckGoSearchRun(name="search")


## Sidebar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter Your Groq API KEY", type= "password")

st.title("🔎 LangChain Chat with Search" )
"""
In this Example, we're using 'streamlitClallBackHandler' to display the thoughts and actions .
Try more 🤝 langchain streamlit agents example at [github.com/langchain-ai/streamlit-agent]

"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I am a chatbot who can search the web. How can i Help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    

    llm = ChatGroq(groq_api_key= api_key, model="Llama3.2-8b-8192", streaming=True)
    tools = [search, arxive, wikipedia]
    search_agent = initialize_agent(tools, llm, agent=agent_types.AgentType.ZERO_SHOT_REACT_DESCRIPTION)



    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

