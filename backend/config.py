from dotenv import load_dotenv
import os

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")