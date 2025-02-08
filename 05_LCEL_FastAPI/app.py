# Streamlit Translation Interface
import requests
import streamlit as st

def get_groq_response(input_text):
   json_body = {
       "input": {
           "language": "French",
           "text": input_text
       }
   }
   response = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)
   return response.json()

# Streamlit app
st.title("LLM Application Using LCEL")
input_text = st.text_input("Enter the text you want to convert to french")

if input_text:
   st.write(get_groq_response(input_text))

# To run:
# 1. Make sure FastAPI server is running (uvicorn main:app --reload)
# 2. Open new terminal and run: streamlit run app.py
# 3. Open browser at http://localhost:8501