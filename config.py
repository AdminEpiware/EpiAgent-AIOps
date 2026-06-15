import os
from dotenv import load_dotenv

load_dotenv()

SPLUNK_HOST = os.getenv("SPLUNK_HOST", "localhost")
SPLUNK_PORT = int(os.getenv("SPLUNK_PORT", "8089"))
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME", "")
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD", "")
SPLUNK_INDEX = os.getenv("SPLUNK_INDEX", "epiagent")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
AI_ENABLED = os.getenv("AI_ENABLED", "true").lower() == "true"
