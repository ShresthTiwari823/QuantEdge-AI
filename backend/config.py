from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=DOTENV_PATH, override=False)

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")