import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

# Configure the Streamlit app
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")


# Sidebar input for Groq API Key
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")
if not groq_api_key:
    st.info("Please add your Groq API key to continue.")
    st.stop()

# Initialize the language model using Groq API
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)



# Initialize Wikipedia search tool
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="A tool for searching the Internet to find various information on the topics mentioned."
)


# Initialize the Math solving tool
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math-related questions. Only mathematical expressions need to be provided."
)


# Define the reasoning prompt template
prompt = """
You are an agent tasked with solving users' mathematical questions. Logically arrive at the solution and provide a detailed explanation,
displaying it point-wise for the question below:
Question: {question}
Answer:
"""
prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)



# Combine the tools into a reasoning chain
chain = LLMChain(llm=llm, prompt=prompt_template)

reasoning_tool = Tool(
    name="Reasoning tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)



# Initialize the assistant agent
assistant_agent = initialize_agent(
    tools=[wikipedia_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)


# Initialize chat session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your math questions."}
    ]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# User interaction: Input question and generate response
question = st.text_area(
    "Enter your question:",
    "Example, I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. "
    "Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?"
)

# Button to process the question
if st.button("Find my answer"):
    if question:
        with st.spinner("Generating response..."):
            # Add user question to session state
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            # Generate the response using the assistant agent
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])

            # Add assistant response to session state and display it
            st.session_state.messages.append({'role': 'assistant', "content": response})
            st.write('### Response:')
            st.success(response)
    else:
        st.warning("Please enter the question.")
