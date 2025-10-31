import random
from asyncio import Lock
from collections import defaultdict

from cachetools import LRUCache
from database.methods import get_channel_by_nick, get_random_channel, update_channel_summary
from llm_manager.summary import get_summary

from utils.log_manager import log_manager


class CacheManager:
    def __init__(self, max_cache_size=100, max_user_history=50):
        self.channel_cache: LRUCache = LRUCache(maxsize=max_cache_size)
        self.user_history: defaultdict = defaultdict(set)
        self.cache_lock = Lock()
        self.max_user_history = max_user_history

    async def get_channel_with_summary_from_cache(self, user_id: int) -> tuple[str, str] | tuple[None, None]:

        async with self.cache_lock:
            available_channels = [
                channel for channel in self.channel_cache
                if channel not in self.user_history[user_id]
            ]

            if available_channels:
                chosen_channel = random.choice(available_channels)
                summary = self.channel_cache[chosen_channel]
                self.user_history[user_id].add(chosen_channel)
                if len(self.user_history[user_id]) > self.max_user_history:
                    oldest_key = next(iter(self.user_history[user_id]))
                    self.user_history[user_id].discard(oldest_key)
                    log_manager.log_system_event('User history trimmed', data={'user_id': user_id})

                log_manager.log_system_event(
                    'Channel from cache for user',
                    data={
                        'user_id': user_id,
                        'cache size': len(self.channel_cache),
                        'picked from_cache': chosen_channel,
                        'user_history_size': len(self.user_history[user_id])
                    }
                )
                return chosen_channel, summary

            log_manager.log_system_event(
                'Cache empty or all channels seen by user, fetching new',
                data={'user_id': user_id, 'cache size': len(self.channel_cache), 'user_history_size': len(self.user_history[user_id])}
            )

        new_channel_nick = await get_random_channel()

        async with self.cache_lock:
            if new_channel_nick in self.user_history[user_id]:
                 pass

            if new_channel_nick in self.channel_cache:
                summary = self.channel_cache[new_channel_nick]
                self.user_history[user_id].add(new_channel_nick)
                if len(self.user_history[user_id]) > self.max_user_history:
                    oldest_key = next(iter(self.user_history[user_id]))
                    self.user_history[user_id].discard(oldest_key)
                log_manager.log_system_event(
                    'Channel from cache (already existed) for user',
                    data={'user_id': user_id, 'picked from_cache': new_channel_nick}
                )
                return new_channel_nick, summary

        db_channel = await get_channel_by_nick(new_channel_nick)

        if db_channel and db_channel.summary:
            summary = db_channel.summary
        else:
            summary = await get_summary(new_channel_nick)
            if len(summary) < 50:
                summary = None
            await update_channel_summary(new_channel_nick, summary)

        async with self.cache_lock:
            self.channel_cache[new_channel_nick] = summary
            self.user_history[user_id].add(new_channel_nick)
            if len(self.user_history[user_id]) > self.max_user_history:
                oldest_key = next(iter(self.user_history[user_id]))
                self.user_history[user_id].discard(oldest_key)
            log_manager.log_system_event(
                'Added new channel to cache and user history',
                data={
                    'user_id': user_id,
                    'cache size': len(self.channel_cache),
                    'added to cache': new_channel_nick,
                    'user_history_size': len(self.user_history[user_id])
                }
            )

        return new_channel_nick, summary

cache_manager = CacheManager()
