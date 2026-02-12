import modal
import os
# Database URL
supabase_secret = modal.Secret.from_name("supabase-credentials")

# Embedding Model
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
EMBEDDING_MODEL_FILE = "onnx/model.onnx"
EMBEDDING_DIM = 384  # dimension for this model
TOP_K_DEFAULT = 5
SIMILARITY_THRESHOLD = 0.0

def get_db_url() -> str:
    """Only call this inside a Modal function, never at module level."""
    return os.environ["PG_URL"]
