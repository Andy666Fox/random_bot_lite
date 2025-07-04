from sqlalchemy.sql.expression import func
from sqlalchemy import select, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
import asyncpg
from schemas import Channel, db_url
from session_gen import get_session
import random
import csv
from tqdm import tqdm


async def get_random_channel():
    try:
        async with get_session() as session:
            count_stmt = select(func.count(Channel.id)).where(Channel.channel_status==1)
            count_result = await session.execute(count_stmt)
            total_count = count_result.scalar()

            if total_count == 0:
                return None
            
            random_offset = random.randint(0, total_count-1)

            stmt = (select(Channel.channelnick)
                    .where(Channel.channel_status==1)
                    .offset(random_offset)
                    .limit(1))
            result = await session.execute(stmt)
            channel_nick = result.scalar_one_or_none()
            return channel_nick
        
    except Exception as e:
        print(f'Processing failed: {e}')
        return None


async def insert_channels_from_csv(csv_file_path: str, batch_size=500):
    data = []
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append((row[0], int(row[1])))

    total_rows = len(data)
    inserted_count = 0
    connection_uri = db_url.replace("+asyncpg", '')
    print(connection_uri)
    conn = await asyncpg.connect(connection_uri)
    with tqdm(total=total_rows, desc='Inserting data...') as pbar:
        for i in range(0, total_rows, batch_size):
            batch = data[i:i+batch_size]
            values = []
            params = []

            for idx, (nick, status) in enumerate(batch, start=1):
                base_idx = idx * 2 - 1
                values.append(f"(${base_idx}::VARCHAR, ${base_idx+1}::INTEGER)")
                params.extend([nick, status])

            query = f"""
                INSERT INTO channels (channelnick, channel_status)
                VALUES {','.join(values)}
                """
                
            try:
                await conn.execute(query, *params)
                inserted_count += len(batch)
                pbar.update(len(batch))  # Обновляем прогресс-бар
            except Exception as e:
                print(f"\nОшибка при вставке пакета {i}-{i+len(batch)}: {str(e)}")

    await conn.close()
    print(f'Success: {inserted_count} rows inserted')
        

