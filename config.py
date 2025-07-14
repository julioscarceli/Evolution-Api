import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

EVOLUTION_BASE_URL = os.getenv("EVOLUTION_BASE_URL")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")
EVOLUTION_TOKEN = os.getenv("EVOLUTION_TOKEN")
PORT = int(os.getenv("PORT", 8000))