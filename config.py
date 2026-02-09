from dotenv import load_dotenv
from pathlib import Path
import os

#os.environ["HF_HUB_OFFLINE"] = "1"

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
embd_model_name = "intfloat/multilingual-e5-small"#"sentence-transformers/all-MiniLM-L6-v2"

# RAG threshold
RAG_THR = 0.45
RAG_K = 10


# Model
LLMNAME="mistralai/Mistral-7B-Instruct-v0.2"

qna_model_name = "timpal0l/mdeberta-v3-base-squad2"

system_prompt_template = {
    'A' : """
        Assistant IA de la Communauté de Communes Val de Loire Numérique. 
        Réponds **uniquement** aux questions sur : état civil, urbanisme, déchets, transports, petite-enfance, social, vie associative, élections, logement, culture/sport, fiscalité, eau/assainissement.
        
        Question : {query}

        **Règles :**
        - Langue : français uniquement.
        - Si la question est dans ce périmètre, répond en 1-2 phrases maximum. 
        - Si hors-périmètre, réponds **uniquement** : "Ce sujet ne fait pas partie de mon périmètre."

    """,
    'B' : """
        Tu es l'assistant de la Communauté de Communes Val de Loire Numérique.

        Contexte :
        {context}

        Question : {query}

        Si le contexte contient la réponse :
        - Réponds en français (vouvoiement), 2-4 phrases, puis "Sources : [doc_ids]"

        Si le contexte ne contient PAS la réponse :
        - Réponds uniquement : "Je n'ai pas trouvé d'information sur ce sujet."
        """,

    'C' : "{context}"
}

# Benchmark results path
BENCHMARK_RESULTS = DATA_DIR / "benchmark_results.parquet"