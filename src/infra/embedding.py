import modal
from .app import app
from .image import image
from .config import (
    supabase_secret,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
    EMBEDDING_MODEL_FILE,
)


@app.cls(
    image=image,
    min_containers=1,
    secrets=[supabase_secret],
)
class EmbeddingService:
    @modal.enter()
    def setup(self):
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
        self.model = TextEmbedding(model_name=EMBEDDING_MODEL)

    @modal.method()
    def embed(self, text: str) -> list[float]:
        embedding = next(self.model.embed([text]))
        return embedding.tolist()

    @modal.method()
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = list(self.model.embed(texts))
        return [e.tolist() for e in embeddings]