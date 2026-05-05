import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Carrega o .env
load_dotenv()

# Caminhos Base
BASE_DIR = Path(__file__).parent.parent
STATUS_FILE = BASE_DIR / "status_api.json"

# Configurações de API (Lidas do .env)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")

# Configurações de Fallback
FALLBACK_DURATION = timedelta(hours=24)