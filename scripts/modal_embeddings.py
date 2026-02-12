import asyncio
import json

from config import postgres
import asyncpg
import modal

def format_document(document):
    text = f"passage: {document['question']} {document['answer']} {document['keywords']}"

    return text


async def main():
    # Call your Modal embedding service
    EmbeddingService = modal.Cls.from_name("retrieval-service", "EmbeddingService")

    conn = await asyncpg.connect(**postgres)

    try:
        # Fetch documents without embeddings
        rows = await conn.fetch(
            "SELECT id, content FROM documents WHERE embedding IS NULL"
        )
        print(f"Found {len(rows)} documents to embed")

        for row in rows:
            # Call Modal remotely
            text = format_document(json.loads(row['content']))
            embedding = EmbeddingService().embed.remote(text)
            
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