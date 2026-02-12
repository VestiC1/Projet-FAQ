import modal
from .app import app
from .image import image
from .config import get_db_url, supabase_secret, TOP_K_DEFAULT, SIMILARITY_THRESHOLD


@app.function(
    image=image,
    secrets=[supabase_secret],
)
@modal.fastapi_endpoint(method="POST") 
async def retrieve(item: dict):
    import asyncpg
    from .embedding import EmbeddingService 

    query = item["query"]
    top_k = item.get("top_k", TOP_K_DEFAULT)
    threshold = item.get("threshold", SIMILARITY_THRESHOLD)

    service = EmbeddingService()
    embedding = service.embed.remote(query)

    embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"

    conn = await asyncpg.connect(get_db_url(), statement_cache_size=0)
    try:
        rows = await conn.fetch(
            "SELECT * FROM match_documents($1, $2, $3)",
            embedding_str,
            top_k,
            threshold,
        )
        return {
            "results": [
                {
                    "id": str(row["id"]),
                    "content": row["content"],
                    "similarity": row["similarity"],
                }
                for row in rows
            ]
        }
    finally:
        await conn.close()