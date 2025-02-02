import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from yt_dlp import YoutubeDL

## Streamlit APP Configuration
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize URL")

"""
Created by Duygu Jones
"""

## Sidebar for Groq API Key and URL Input
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

generic_url = st.text_input("Enter URL (YouTube or Website)", label_visibility="collapsed")

## Initialize Gemma Model Using Groq API
llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

## Prompt Template for Summarization
prompt_template = """
Provide a summary of the following content in 300 words:
Content:{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

## Function to Handle YouTube Videos Using yt-dlp
def fetch_youtube_transcript(url):
    ydl_opts = {"noplaylist": True, "quiet": True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("description", "No transcript or description available.")
    except Exception as e:
        st.error(f"Error fetching YouTube video: {e}")
        return None

## Summarization Process
from langchain.docstore.document import Document

if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the API key and URL to proceed.")
    elif not validators.url(generic_url):
        st.error("Invalid URL. Please provide a valid YouTube or Website URL.")
    else:
        try:
            with st.spinner("Processing..."):
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    content = fetch_youtube_transcript(generic_url)
                    if content is None:
                        st.error("Failed to fetch YouTube content.")
                        st.stop()
                    docs = [Document(page_content=content)]
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        },
                    )
                    # Load website content as Document objects
                    docs = loader.load()

                # Chain for Summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception occurred: {e}")

# ### Code Flow:
# 1. Set up Streamlit interface and configuration
# 2. Get Groq API key and URL input from user
# 3. Initialize Gemma model and create prompt template
# 4. Process URL content (YouTube or website)
# 5. Generate and display summary
# 6. Handle errors and exceptions

# To run:
# 1. Install required packages: streamlit, langchain, validators, yt-dlp
# 2. Set up Groq API key
# 3. Run: streamlit run app.py
# 4. Access the app at http://localhost:8501
