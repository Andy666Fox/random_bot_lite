import random
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import text
from utils.log_manager import log_manager
from utils.math_manager import math_manager

from database.schemas import Channel, Rating, User
from database.session_gen import get_session


async def get_random_channel(limit: int = 1):
    try:
        async with get_session() as session:
            min_max_result = await session.execute(text("SELECT MIN(id), MAX(id) FROM channels"))
            min_id, max_id = min_max_result.fetchone()

            if min_id is None or max_id is None:
                return None

            random_id = random.randint(min_id, max_id)

            stmt = (
                select(Channel.channelnick)
                .where(Channel.id >= random_id)
                .order_by(Channel.id)
                .limit(limit)
            )
            result = await session.execute(stmt)
            channel = result.scalar_one_or_none()

            if channel:
                return channel

    except Exception as e:
        print(f"Processing failed: {e}")
        log_manager.log_error(e, context={"get_random_channel_func_error": e})
        return None


async def insert_suggested_channel(channelnick: str):
    try:
        async with get_session() as session:
            suggestion = Channel(channelnick=channelnick, status=1, avg_score=5.0)
            session.add(suggestion)
            await session.commit()
            await session.refresh(suggestion)
            return True, "created"
    except IntegrityError:
        return False, "exists"
    except Exception as e:
        print(f"Inserting failed: {e}")
        log_manager.log_error(e, context={"insert_suggested_channel_func_error": e})
        return False, "error"


async def insert_user(user_id: int, nickname: str):
    try:
        async with get_session() as session:
            result = await session.execute(select(User).where(User.telegram_id == user_id))
            user = result.scalar_one_or_none()

            if user:
                return False
            else:
                new_user = User(
                    telegram_id=user_id,
                    nickname=nickname,
                    last_online=datetime.now(UTC),
                )
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                return True
    except Exception as e:
        print(f"Inserting failed: {e}")
        log_manager.log_error(e, context={"insert_user_func_error": e})
        return False


async def update_channel_rating(channelnick: str, score: int):
    try:
        async with get_session() as session:
            result = await session.execute(
                select(Channel, Rating)
                .join(Rating, Channel.id == Rating.channel_id, isouter=True)  # LEFT JOIN
                .where(Channel.channelnick == channelnick)
            )
            row = result.first()

            channel, rating = row

            if rating is None:
                new_rating = Rating(
                    channel_id=channel.id,
                    likes=5 if score == 1 else 4,  # Инициализация
                    dislikes=5 if score == -1 else 4,
                )
                session.add(new_rating)
                await session.flush()
                rating = new_rating
            else:
                if score == 1:
                    rating.likes += 1
                elif score == -1:
                    rating.dislikes += 1

            await session.commit()
            await _update_channel_avg_score(channelnick)
            return True
    except Exception as e:
        log_manager.log_error(e, context={"update_channel_rating_func_error": e})
        return False


async def _update_channel_avg_score(channelnick: str):
    try:
        async with get_session() as session:
            result = await session.execute(
                select(Channel, Rating)
                .join(Rating, Channel.id == Rating.channel_id)
                .where(Channel.channelnick == channelnick)
            )

            row = result.first()
            channel, rating = row
            bscore = await math_manager.get_bavg_score(rating.likes, rating.dislikes)
            log_manager.log_system_event(
                "channel score updated",
                data={
                    "channel score": f"{channelnick} score changed from \
                                       {channel.avg_score} to {bscore}"
                },
            )

            channel.avg_score = bscore
            await session.commit()
        return True
    except Exception as e:
        log_manager.log_error(e, context={"update_avg_score_func_error": channelnick})
        return False


async def update_channel_summary(channelnick: str, summary: str):
    try:
        async with get_session() as session:
            result = await session.execute(
                select(Channel).where(Channel.channelnick == channelnick)
            )
            channel = result.scalar_one_or_none()

            if channel.summary:
                return False

            channel.summary = summary
            await session.commit()

            log_manager.log_system_event(
                "channel summary updated",
                data={"summary updated": f"{channelnick} summary updated"},
            )
            return True

    except Exception as e:
        print(f"Inserting failed: {e}")
        log_manager.log_error(e, context={"insert_channel_summary_func_error": e})
        return False


async def get_channel_by_nick(channelnick: str):
    try:
        async with get_session() as session:
            result = await session.execute(
                select(Channel).where(Channel.channelnick == channelnick)
            )
            return result.scalar_one_or_none()

    except Exception as e:
        print(f"Getting failed: {e}")
        log_manager.log_error(e, context={"get_channel_by_nick_func_error": e})
        return False


async def get_db_stats():
    try:
        async with get_session() as session:
            total_channels = await session.scalar(select(func.count(Channel.id)))

            status_stats = await session.execute(
                select(Channel.status, func.count(Channel.id)).group_by(Channel.status)
            )
            status_dict = {status: count for status, count in status_stats.all()}

            active_status_ratio = (status_dict[1] / total_channels) * 100

            total_users = await session.scalar(select(func.count(User.id)))

            time_window = datetime.now() - timedelta(days=15)
            active_users = await session.scalar(
                select(func.count(User.id)).where(User.last_online >= time_window)
            )

            return [total_channels, active_status_ratio, total_users, active_users]
    except Exception as e:
        log_manager.log_error(e, context={"get_db_stats_func_error": str(e)})
        return {}
