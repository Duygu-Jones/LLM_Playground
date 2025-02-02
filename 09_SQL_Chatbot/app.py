import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq


# Configure Streamlit page
st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

# Define database types
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# Get database selection from user
radio_opt = ["Use SQLLite3 Database - Student.db", "Connect to you MySQL Database"]
selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat", options=radio_opt)

# If MySQL is selected, get login credentials
if radio_opt.index(selected_opt) == 1:
   db_uri = MYSQL
   mysql_host = st.sidebar.text_input("Provide MySQL Host")
   mysql_user = st.sidebar.text_input("MYSQL User")
   mysql_password = st.sidebar.text_input("MYSQL password", type="password")
   mysql_db = st.sidebar.text_input("MySQL database")
else:
   db_uri = LOCALDB

# Get API key
api_key = st.sidebar.text_input(label="GRoq API Key", type="password")

# User alerts
if not db_uri:
   st.info("Please enter the database information and uri")
if not api_key:
   st.info("Please add the groq api key")

# Define LLM model
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# Database configuration function
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
   
   if db_uri == LOCALDB:
       # SQLite database connection
       dbfilepath = (Path(__file__).parent / "student.db").absolute()
       creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
       return SQLDatabase(create_engine("sqlite:///", creator=creator))
   
   elif db_uri == MYSQL:
       # MySQL connection check
       if not (mysql_host and mysql_user and mysql_password and mysql_db):
           st.error("Please provide all MySQL connection details.")
           st.stop()
       return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
       #for postgresql: SQLDatabase(create_engine("postgresql+psycopg2://username:password@localhost:5432/database_name"))

# Create connection based on selected database
if db_uri == MYSQL:
   db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
   db = configure_db(db_uri)

# Create SQL toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Create SQL agent
agent = create_sql_agent(
   llm=llm,
   toolkit=toolkit,
   verbose=True,
   agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Check and clear message history
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
   st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Show message history to user
for msg in st.session_state.messages:
   st.chat_message(msg["role"]).write(msg["content"])

# Get query from user
user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
   # Add query to message history
   st.session_state.messages.append({"role": "user", "content": user_query})
   st.chat_message("user").write(user_query)

   with st.chat_message("assistant"):
       # Process query and return results
       streamlit_callback = StreamlitCallbackHandler(st.container())
       response = agent.run(user_query, callbacks=[streamlit_callback])
       st.session_state.messages.append({"role": "assistant", "content": response})
       st.write(response)

# ### **General Flow Summary**
# 1. User selects either SQLite or MySQL database
# 2. Database connection is configured based on selection
# 3. Groq API key is obtained from user and an LLM model is configured
# 4. LangChain toolkit and agent are defined to convert natural language queries to database queries
# 5. Queries from user are processed and results are returned to the user

# To run:
# 1. Create a virtual environment and activate it
#    python -m venv venv
#    source venv/bin/activate (Linux/Mac)
#    venv\Scripts\activate (Windows)
# 2. Install required packages
#    pip install -r requirements.txt
# 3. Set up your .env file with API keys
#    GROQ_API_KEY=your_key_here
# 4. Run the Streamlit app
#    streamlit run app.py
# 5. Open browser at http://localhost:8501