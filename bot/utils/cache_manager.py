import random
from cachetools import LRUCache
from asyncio import Lock 
from typing import Tuple

from llm_manager.summary import get_summary
from log_manager import log_manager
from database.methods import (
    get_random_channel,
    get_channel_by_nick,
    update_channel_summary
)


class CacheManager():
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.channel_cache: LRUCache = LRUCache(maxsize=100)
        self.cache_lock = Lock()

    async def get_channel_with_summary_from_cache(self, user_id: int) -> Tuple[str, str]:
        async with self.cache_lock:
            if len(self.channel_cache) > 0:
                channel = random.choice(list(self.channel_cache.keys()))
                log_manager.log_system_event('Channel from cache', data={'cache size': len(self.channel_cache), 'picked from_cache': channel})
                return channel, self.channel_cache[channel]
            
        channel = await get_random_channel()

        async with self.cache_lock:
            if channel in self.channel_cache:
                return channel, self.channel_cache[channel]
            
        db_channel = await get_channel_by_nick(channel)

        if db_channel and db_channel.summary:
            summary = db_channel.summary
        else:
            summary = await get_summary(channel)
            await update_channel_summary(channel, summary)
        
        async with self.cache_lock:
            self.channel_cache[channel] = summary
            log_manager.log_system_event('Added to cache', data={'cache size': len(self.channel_cache), 'added to cache': channel})

        return channel, summary
    
cache_manager = CacheManager()