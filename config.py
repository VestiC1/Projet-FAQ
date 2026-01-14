from dotenv import load_dotenv
from pathlib import Path
import os

# Project root directory
ROOT = Path(__file__).parent

# Secrets loading
load_dotenv( dotenv_path=ROOT / ".env", override=True )

# Data directory
DATA_DIR = ROOT / "data"

# Data file paths
FAQ_PATH    = DATA_DIR / "faq-base-6964b97cf0c25947575840.json"
GOLDEN_PATH = DATA_DIR / "golden-set-6964b9874cff1935078155.json"
# Embeddings FAQ
FAQ_VEC = DATA_DIR / "faq_embeddings.parquet"

# Expose les variables nécessaires
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("Le token Hugging Face (HF_TOKEN) n'est pas défini dans le fichier .env.")

# Embedding model name
embd_model_name = "sentence-transformers/all-MiniLM-L6-v2"

# RAG threshold
RAG_THR = 0.45
RAG_K = 5