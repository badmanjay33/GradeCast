from google import genai
import os
from dotenv import load_dotenv


load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def prompt(text):
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=text
    )
    return response.text
