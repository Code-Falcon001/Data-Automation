import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a local .env file
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent
CV_PATH = BASE_DIR / "CV.pdf"
EXCEL_TRACKER_PATH = BASE_DIR / "job_applications.xlsx"

# OpenClaw Settings (compatible with local OpenAI setups)
OPENCLAW_API_BASE = os.getenv("OPENCLAW_API_BASE", "http://127.0.0.1:18789/v1")
OPENCLAW_MODEL = os.getenv("OPENCLAW_MODEL", "openclaw")
OPENCLAW_API_KEY = os.getenv("OPENCLAW_API_KEY", "e8804d5c6eb1ebb35ec296223743e6e0f4e48a41558a9deb")

# Scraping Settings
MIN_MATCH_SCORE = int(os.getenv("MIN_MATCH_SCORE", "0"))
TARGET_JOB_COUNT = int(os.getenv("TARGET_JOB_COUNT", "50"))
