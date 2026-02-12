import asyncio
import json
import os

import asyncpg
import modal


async def main():
    # Call your Modal embedding service
    EmbeddingService = modal.Cls.from_name("retrieval-service", "EmbeddingService")

    conn = await asyncpg.connect(os.environ["SUPABASE_DB_URL"])

    try:
        # Fetch documents without embeddings
        rows = await conn.fetch(
            "SELECT id, text FROM documents WHERE embedding IS NULL"
        )
        print(f"Found {len(rows)} documents to embed")

        for row in rows:
            # Call Modal remotely
            embedding = EmbeddingService().embed.remote(row["text"])

            await conn.execute(
                "UPDATE documents SET embedding = $1 WHERE id = $2",
                json.dumps(embedding),
                row["id"],
            )
            print(f"  ✓ {row['id']}")

        print(f"✓ {len(rows)} embeddings generated")

    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())