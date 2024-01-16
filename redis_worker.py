from config import REDIS_HOST, REDIS_PORT, REDIS_DB
from redis import asyncio as aioredis


r = aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


async def check_availability():
    return await r.ping()
