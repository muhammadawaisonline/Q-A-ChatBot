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
st.title("Text to math problem Solver with Gamma2")

groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not groq_api_key:
    st.info("Please Add Your Groq API Key to Continue.")
    st.stop()

llm = ChatGroq(model="Gemma2-9b-It", groq_api_key= groq_api_key)

##Initializing the tool
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="wikipedia",
    func= wikipedia_wrapper.run(),
    description= "A tool for searching the internet to find the various information on the given question"
)

#Initializing Math Tool
math_chain = LLMMathChain(llm=llm)
calculator= Tool(
    name="calculator",
    func=math_chain.run(),
    description="A Tool for answering math related questions.only input mathematical expression need to be provided."
) 

prompt = """
You are agent solving users mathematical questions. Logically arrive at the solutions and provide a detail explanations
and display it point wise at the below questions
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

## Combining all the tools into chain
chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)

reasoning_tool = Tool(
    name= "Reasoning tool",
    func=chain.run(),
    description= "A tool for answering logic-based and reasoning questions."

)

## Initializing the agent
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose= False,
    handle_parsing_errors = True
)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi I am math chatbot who can answer all your maths questions"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

## Lets start the intraction 
question = st.text_area("Enter your questions: ", "I have 5 bananas and 7 grapes I eat 2 bananas shahzad piced up 1 grapes but islam eata half garpe. How many bananas and grapes left behind?")

if st.button("Find My Answer"):
    if question:
        with st.spinner("Generate Response ..."):
            st.session_state.messages.append({"role":"user", "content": {question}})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state.messages, callbacks= [st_cb])
            
            st.session_state.messages.append({"role":"assistant", "content":response})
            st.write("### Respnse..")
            st.success(response)
    else:
        st.warning("Please enter the question")