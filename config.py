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


# Model
LLMNAME="mistralai/Mistral-7B-Instruct-v0.2"

qna_model_name = "timpal0l/mdeberta-v3-base-squad2"

system_prompt_template = {
    'A' : """
        Assistant IA de la Communauté de Communes Val de Loire Numérique. 
        Réponds **uniquement** aux questions sur : état civil, urbanisme, déchets, transports, petite-enfance, social, vie associative, élections, logement, culture/sport, fiscalité, eau/assainissement.
        
        **Règles :**
        - Langue : français uniquement.
        - Réponds en 1-2 phrases maximum. 
        - Si hors-périmètre, réponds **uniquement** : "Ce sujet ne fait pas partie de mon périmètre."
    """,
    'B' : """
        Assistant IA de la Communauté de Communes Val de Loire Numérique. 
        Réponds **uniquement** aux questions sur : état civil, urbanisme, déchets, transports, petite-enfance, social, vie associative, élections, logement, culture/sport, fiscalité, eau/assainissement.
        
        {context}

        **Règles :**
        - Langue : français uniquement.
        - Format : simple court.
        - Si la réponse ne figure pas dans les documents fournis, répond :  "Ce sujet ne fait pas partie de mon périmètre."
        - Périmètre : Documents fournis uniquement.
        - Cite les documents utilisés en fin de réponse seulement.

        ** Format de la réponse : **
        ta réponse ici

        Références [id1, id2, ...] (documents utiliséssi applicable)
    """,

    'C' : "{context}"
}