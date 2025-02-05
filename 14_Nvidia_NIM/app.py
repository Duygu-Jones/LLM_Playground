import streamlit as st
import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
import time

from dotenv import load_dotenv
load_dotenv()

# Load the NVIDIA API Key from the environment variables
os.environ['NVIDIA_API_KEY'] = os.getenv("NVIDIA_API_KEY")


# Function to handle document embedding and vector creation
def vector_embedding():
    if "vectors" not in st.session_state:
        # Initialize embeddings using NVIDIAEmbeddings
        st.session_state.embeddings = NVIDIAEmbeddings()

        # Load documents from a directory containing PDF files
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")
        st.session_state.docs = st.session_state.loader.load()

        # Split documents into smaller chunks for processing
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(
            st.session_state.docs[:30]
        )  # Only process the first 30 documents for efficiency

        # Create vector embeddings for the documents
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)


# Streamlit app title
st.title("NVIDIA-Powered Document Query Bot")

# Initialize the language model with a specific model
llm = ChatNVIDIA(model="meta/llama3-70b-instruct")

# Define the prompt template for the chatbot
prompt = ChatPromptTemplate.from_template(
    """
Answer the questions based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Questions:{input}

"""
)

# Input field for the user's question
prompt1 = st.text_input("Enter Your Question From Documents")

# Button to start the document embedding process
if st.button("Documents Embedding"):
    vector_embedding()
    st.write("Vector Store DB Is Ready")

# If the user has entered a question
if prompt1:
    # Create a chain for combining documents and processing them with the model
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Retrieve vectors for similarity search
    retriever = st.session_state.vectors.as_retriever()

    # Create a retrieval chain for finding and processing relevant documents
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Measure the response time
    start = time.process_time()
    response = retrieval_chain.invoke({'input': prompt1})
    print("Response time:", time.process_time() - start)

    # Display the response
    st.write(response['answer'])

    # With a Streamlit expander, display the relevant documents and their similarity scores
    with st.expander("Document Similarity Search"):
        # Perform similarity search with scores
        results = st.session_state.vectors.similarity_search_with_score(prompt1, k=4)

        for i, (doc, score) in enumerate(results):
            st.write(f"**Document {i+1}**")            
            st.write(f"Similarity Score: {score:.4f}")
            st.write(f"Content: {doc.page_content}")
            st.write("--------------------------------")
