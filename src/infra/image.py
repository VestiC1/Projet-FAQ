import modal
from .config import EMBEDDING_MODEL, EMBEDDING_MODEL_FILE, EMBEDDING_DIM

def download_model():
    from fastembed import TextEmbedding
    from fastembed.common.model_description import PoolingType, ModelSource

    TextEmbedding.add_custom_model(
        model=EMBEDDING_MODEL,
        pooling=PoolingType.MEAN,
        normalization=True,
        sources=ModelSource(hf=EMBEDDING_MODEL),
        dim=EMBEDDING_DIM,
        model_file=EMBEDDING_MODEL_FILE,
    )
    # Triggers download and caches the ONNX model
    TextEmbedding(model_name=EMBEDDING_MODEL)


image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install(
        "fastembed",
        "numpy",
        "asyncpg",
        "fastapi[standard]",
    )
    .run_function(download_model)
)