import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    REPO_NAME = os.getenv("REPO_NAME")
    DB_NAME = "sqlite:///code_hunter.db"
    
    if not GITHUB_TOKEN or not GOOGLE_API_KEY:
        raise ValueError("Variáveis de ambiente no arquivo .env, não carregadas corretamente")