import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

STATUS_FILE = BASE_DIR / "status_api.json"
MEMORIA_FILE = BASE_DIR / "memoria.json"
SKILLS_DIR = BASE_DIR / "skills"

SKILLS_DIR.mkdir(parents=True, exist_ok=True)
(SKILLS_DIR / "__init__.py").touch(exist_ok=True)

# Chaves de API
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# Modelos
TOGETHER_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
GEMINI_MODEL = "gemini-2.5-flash"
OLLAMA_MODEL = "qwen2.5-coder:7b"
OLLAMA_URL = "http://localhost:11434/api/chat"