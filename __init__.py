import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Grab API key from .env
api_key = os.getenv("Trying to read GOOGLE_API_KEY from env...") 

api_key = os.getenv("GOOGLE_API_KEY")
print(api_key)

if not api_key:
    raise ValueError("API key missing. Add it to .env")

# Configure Gemini with the API key
genai.configure(api_key=api_key)

# Example: make sure it works
model = genai.GenerativeModel("gemini-1.5-flash")

# Test message (you can remove this after checking)
response = model.generate_content("Hello Gemini from unhingedmf!")
print(response.text)

