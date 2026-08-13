from google import genai
import os
from dotenv import load_dotenv
from google.genai import errors  # Import the new SDK's specific error module

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def prompt(text):
    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=text
        )
        return response.text
    except errors.APIError:  # Catch the correct error type
        return "AI Advisor is currently unavailable. The server is busy."
    except Exception as e: # Optional: A final safety net for internet drops
        print(f"Connection failed: {e}")
        return "Failed to connect to the AI Advisor. Please check your internet connection."