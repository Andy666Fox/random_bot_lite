from sqlalchemy.sql.expression import func
from sqlalchemy import select, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database.schemas import Channel
from database.database import get_session
import json 
import random


async def get_random_channel():
    try:
        async with get_session() as session:
            count_stmt = select(func.count(Channel.id)).where(Channel.channel_status==1)
            count_result = await session.execute
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


async def insert_channels_from_json(json_file_path: str, replace_existing: bool = False):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            channels_data = json.load(file)

        channels_to_insert = []
        for channel_nick, channel_status in channels_data.items():
            channels_to_insert.append({'channelnick': channel_nick,
                                       'channel_status': channel_status})
        
        inserted_count = 0
        updated_count = 0
        errors = []
        
        async with get_session() as session:
            if replace_existing:
                stmt = pg_insert(Channel).values(channels_to_insert)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['channelnick'],
                    set_=dict(channel_status=stmt.excluded.channel_status)
                )
                result = await session.execute(stmt)
                await session.commit()

                updated_count = result.rowcount
            else:
                for channel_data in channels_to_insert:
                    try:
                        existing_stmt = select(Channel).where(
                            Channel.channelnick == channel_data['channelnick'])
                        existing_result = await session.execute(existing_stmt)
                        existing_channel = existing_result.scalar_one_or_none()

                        if existing_channel:
                            errors.append(f'Channel {channel_data['channelnick']} exists in table')
                            continue

                        stmt = insert(Channel).values(channel_data)
                        await session.execute(stmt)
                        inserted_count += 1
                    except Exception as e:
                        errors.append(f"Fail to insert {channel_data['channelnick']}: {str(e)}")
                        continue
                
                await session.commit()

        return {
            'succes': True,
            'inserted_count': inserted_count,
            'updated_count': updated_count,
            'total_processed': len(channel_data),
            'errors': errors
        }  
    except Exception as e:
        return {
            'succes': False,
            'error': str(e)
        }

