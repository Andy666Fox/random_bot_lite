import random
from cachetools import LRUCache
from asyncio import Lock 
from typing import Tuple

from llm_manager.summary import get_summary
from log_manager import bot_logger
from database.methods import (
    get_random_channel,
    get_channel_by_nick,
    update_channel_summary
)

channel_cache: LRUCache = LRUCache(maxsize=100)
cache_lock = Lock()

async def get_channel_with_summary_from_cache(user_id: int) -> Tuple[str, str]:
    async with cache_lock:
        if len(channel_cache) > 0:
            channel = random.choice(list(channel_cache.keys()))
            bot_logger.log_system_event('Channel from cache', data={'cache size': len(channel_cache), 'picked from_cache': channel})
            return channel, channel_cache[channel]
        
    channel = await get_random_channel()

    async with cache_lock:
        if channel in channel_cache:
            return channel, channel_cache[channel]
        
    db_channel = await get_channel_by_nick(channel)

    if db_channel and db_channel.summary:
        summary = db_channel.summary
    else:
        summary = await get_summary(channel)
        await update_channel_summary(channel, summary)
    
    async with cache_lock:
        channel_cache[channel] = summary
        bot_logger.log_system_event('Added to cache', data={'cache size': len(channel_cache), 'added to cache': channel})

    return channel, summary