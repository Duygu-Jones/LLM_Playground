# FastAPI Translation Server Setup
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

parser = StrOutputParser()

# Create chain
chain = prompt_template|model|parser

# App definition
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)

# Adding chain routes
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Dependencies:
# langserve
# uvicorn
# fastapi
# sse_starlette
# pydantic
# faiss-cpu
# chromadb
# langchain
# python-dotenv
# ipykernel
# langchain-community
# requests
# streamlit

# To run the server:
# 1. Save this file as 'main.py'
# 2. Run command: uvicorn main:app --reload
# 3. Visit http://127.0.0.1:8000/docs for Swagger UI
# 4. Or test directly at http://127.0.0.1:8000/chain
# 5. Use Ctrl+C to stop the server