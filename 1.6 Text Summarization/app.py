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

prompt_template = """
Provide the summary of the following content in 300 words:
Contenet: {text}
"""
prompt= PromptTemplate(template= prompt_template, input_variables=["text"] )


## Setting us main Page of App
if st.button("Summarize the content from YT or website"):
    ## Validate all type of inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Provide the information to get started.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid url. It may be YT video or website.")
    else:
        try:
            with st.spinner("Waiting..."):
                ## Load the website or yt video data
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info= True)
                else: 
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify= False,
                                                   headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"})
                docs= loader.load()

                ## Chain for summarization 
                chain = load_summarize_chain(llm=llm, 
                                             chain_type="stuff",
                                             prompt= prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exceptions: {e}")
            
