import asyncpg
import json
import os
import asyncio

DB_CONFIG ={
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRESS_PASSWORD"),
    "host": os.getenv("DB_CONTAINER_NAME"),
    "port": 5432
}

JSON_FILE = "/app/bot/db_data/val_channels.json"

async def import_json_data():
    with open(JSON_FILE) as f:
        json_data = json.load(f)

    conn = await asyncpg.connect(**DB_CONFIG)

    try:
        records = [(channel, value) for channel, value in json_data.items()]
        await conn.copy_records_to_table(
            'channels',
            records=records,
            columns=['channelnick', 'id'],
            timeout=10
        )
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(import_json_data())