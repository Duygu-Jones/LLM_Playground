import requests         # Used for making HTTP requests
import json             # Used for working with JSON formatted data
import gradio as gr     # Library used for creating user interface


# API address and URL to be used for sending requests
url = "http://localhost:11434/api/generate"


# Header information to be sent with API request
headers = {
    'Content-Type': 'application/json'  # Indicates that the data is in JSON format
}



history = []   # A list to keep track of user input history

# Function defined to get response from the model
def generate_response(prompt):
    
    history.append(prompt) # Add new user input to history  
    final_prompt = "\n".join(history) # Combine all past inputs into a single text
    
    # JSON data to be sent to API
    data = {
        "model": "CodeBot",         # Model name to be used -> name given in modelfile
        "prompt": final_prompt,     # Text created for the model
        "stream": True             # Indicates that the response should be returned at once, not as a stream
    }
    
    
    # Sending POST request to API
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    # If request is successful, process and return the response
    if response.status_code == 200:
        # Response text is extracted from JSON format and processed
        response = response.text
        data = json.loads(response)
        
        # Main part of the response is extracted and returned
        actual_response = data['response']
        return actual_response
    else:
        print("error:", response.text)    # If there's an error, print error message to console



# Defining Gradio interface
interface = gr.Interface(
    fn=generate_response,       # Function that will process user input
    inputs=gr.Textbox(          # Text box for getting text input from user
        lines=4,                # Text box should be 4 lines long
        placeholder="Enter your Prompt"  # Explanatory text for user
    ),
    outputs="text"              # Response will be returned in text format
)

# Start Gradio application and run on local server
interface.launch()