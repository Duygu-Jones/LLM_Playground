from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

os.environ['NVIDIA_API_KEY']=os.getenv("NVIDIA_API_KEY")

# Check the API key
if not os.environ['NVIDIA_API_KEY']:
    raise ValueError("NVIDIA_API_KEY is not set in the '.env' file. Please check your '.env' configuration.")



client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.environ['NVIDIA_API_KEY']
)

completion = client.chat.completions.create(
  model="meta/llama3-70b-instruct",
  messages=[{"role":"user","content":"hello"}],
  temperature=0.5,
  top_p=1,
  max_tokens=1024,
  stream=True
)

for chunk in completion:
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")

