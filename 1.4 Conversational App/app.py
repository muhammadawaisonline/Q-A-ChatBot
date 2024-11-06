import streamlit as st
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables.history import RunnableWithMessageHistory

os.environ["HUGGINGFACE_TOKEN"] = os.getenv("HUGGINGFACE_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name= "all-MiniLM-L6-v2")

#Setup Streamlit App
st.title("Rag App with Converation Chat History with PDF")
st.write("Ipload PDFs and Chat with their content")

##Input the Qroq API Key
api_key = st.text_input("Enter Your Qroq API Key:", type= "password")

## Check if Qroq Api key is provided.
if api_key:
    llm = ChatGroq(api_key=api_key, model="Gamma2-9b-it")



## Chat Interface
    session_id = st.text_input("Session ID", value= "default_session")

    if "store" not in st.session_state:
        st.session_state.store = {}
    upload_files = st.file_uploader("Choose a pdf files", type= "pdf", accept_multiple_files=True)

    if upload_files:
        documents = []
        for upload_file in upload_files:
            temppdf = f"./temp.pdf"
            with open(temppdf, "wb") as file:
                file.write(upload_file.getvalue())
                file_name = upload_file.name
        loader = PyPDFLoader(temppdf)
        docs = loader.load()
        documents.extend(docs)

    # Split create embddings of uploaded documents
    splitter = RecursiveCharacterTextSplitter(chunk_size= 500, chunk_overlap= 50)
    text_splitter = splitter.split_documents(documents)
    vectorStore = Chroma.from_documents(documents=text_splitter, embedding=embeddings)
    retriever = vectorStore.as_retriever()

    contextualize_q_system_prompt = (
        "Given a chat history and latest user question"
        "which might reference context in the chat History,"
        "formulate the standalone questions which can be understood"
        "without the chat History. Do not answer the question"
        "just fromulate it if needed, otherwise return it as is."
    )
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            "system", contextualize_q_system_prompt,
            MessagesPlaceholder("chat_history"),
            "human", "{input}"
        ]
    )
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)


    #Answer Questions

    #Aswer Questions
    system_prompt = (
        "You are an assistant for question answer talks"
        "use the following pieces of retrieved context to answer"
        "the question, if you don't know the answer, say that you"
        "don't know. Use three sentences maximum and keep the answer"
        "concise"
        "/n/n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history")
            ("human", "{input}")

        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    

