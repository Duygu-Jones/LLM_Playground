import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.tools import Tool
import time
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS  # Different approach using duckduckgo_search directly

# Load environment variables
load_dotenv()

# Initialize Arxiv and Wikipedia tools
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

# Modified search function using DDGS directly
def safe_search(query):
    try:
        time.sleep(1)
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=2))
            if results:
                # Combine the results into a single string
                combined_results = " ".join([result['body'] for result in results])
                return combined_results[:500]  # Limit response length
            return "No results found. Please try a different search query."
    except Exception as e:
        return f"Search error occurred. Please try again with a different query. Error: {str(e)}"

# Define safe search function as a Tool
safe_search_tool = Tool(
    name="Safe Search",
    func=safe_search,
    description="Used for safely searching with DuckDuckGo."
)

# Streamlit title and description
st.title("🔎 LangChain - Chat with Search")
"""
This application shows an agent's thoughts and actions in an interactive Streamlit application using `StreamlitCallbackHandler`.
Visit [LangChain Streamlit Agent](https://github.com/langchain-ai/streamlit-agent) for more examples. [Duygu Jones]
"""

# Sidebar settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

# Store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

# Show historical messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Get user input
if prompt := st.chat_input(placeholder="What is machine learning?"):
    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Initialize Groq language model
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    else:
        llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

        # Define tools
        tools = [safe_search_tool, arxiv, wiki]

        # Create agent
        try:
            search_agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True,
                max_iterations=3  # Add max iterations to prevent infinite loops
            )

            # Generate and display response
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = search_agent.run(prompt, callbacks=[st_cb])  # Changed to use prompt directly
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")