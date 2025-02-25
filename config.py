import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

WOLFRAM_APP_ID = os.getenv("WOLFRAM_APP_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
