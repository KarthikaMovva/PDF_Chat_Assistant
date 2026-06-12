import google.generativeai as genai
from core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

gemini_model = genai.GenerativeModel("gemini-2.5-flash")