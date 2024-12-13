
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from config.config import redis_url


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield