import asyncio
from config import postgres, SCHEMA_FILE, FAQ_PATH
import asyncpg
from src.api.db.load import load_faq
from src.database.crud import create_schema, insert_document

async def main():
    conn = await asyncpg.connect(**postgres, statement_cache_size=0)
    try:
        # Apply schema
        await create_schema(conn=conn, schema=SCHEMA_FILE)
        print("Schema applied")

        # Loading FAQ
        faq_json = load_faq(faq_path=FAQ_PATH)

        # Inserting documents one by one
        inserted = 0
        for document in faq_json.get('faq', []):
            await insert_document(conn=conn, document=document)
            
            inserted += 1

        print(f"{inserted} documents upserted")
        
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())