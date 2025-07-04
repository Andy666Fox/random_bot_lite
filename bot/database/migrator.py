import asyncpg
import json
import os
import asyncio
import time

db_url = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@postgres:5432/{os.getenv("POSTGRES_DB")}'

DB_CONFIG ={
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRESS_PASSWORD"),
    "host": os.getenv("DB_CONTAINER_NAME"),
    "port": 5432
}
time.sleep(20)
JSON_FILE = "/app/bot/db_data/val_channels.json"

async def import_json_data():
    with open(JSON_FILE) as f:
        json_data = json.load(f)

    conn = await asyncpg.connect(db_url)

    try:
        records = [(channel, value) for value, channel in enumerate(json_data.keys())]
        print(records[0])
        await conn.copy_records_to_table(
            'channels',
            records=records,
            columns=['channelnick'],
            timeout=10
        )
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(import_json_data())