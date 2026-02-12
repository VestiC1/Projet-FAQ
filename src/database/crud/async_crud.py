import json
from pathlib import Path

async def create_schema(conn, schema: Path):
    schema = schema.read_text(encoding="utf-8")
    await conn.execute(schema)

async def insert_document(conn, document):

    query = """
            INSERT INTO documents (content)
            VALUES ($1::jsonb);
    """

    await conn.execute(
        query,
        json.dumps(document),
    )
