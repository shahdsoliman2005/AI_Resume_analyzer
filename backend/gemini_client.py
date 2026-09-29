import os
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6IZ5bxZTYSgnDS-bXuiVkIAgjTmjh-FEFBgbozH9yy3mA"))

MODEL_NAME = "gemini-3.6-flash"
EMBEDDING_MODEL_NAME = "gemini-embedding-001"
