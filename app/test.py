import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('YOUR_OPENAI_API_KEY')

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello, world!"}
        ]
    )
    print(response.choices[0].message["content"])
except Exception as e:
    print(f"Error: {e}")
