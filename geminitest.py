import openai
from dotenv import load_dotenv
import os

# ✅ Load API Key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.base_url = "https://openrouter.ai/api/v1"

# ✅ Send test message to OpenRouter
response = openai.ChatCompletion.create(
    model="mistralai/mistral-7b-instruct",  # or try "openai/gpt-3.5-turbo" if available
    messages=[
        {"role": "user", "content": "Hello, who are you?"}
    ]
)

print("OpenRouter says:", response.choices[0].message["content"])
