from redis import Redis
from kink import inject
from services.abstractClasses.serv_cache_i import ICacheService


@inject(alias=ICacheService)
class CacheService(ICacheService):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> str:
        result = self.redis.get(key)
        if result is None:
            raise KeyError(f"Key {key} not found in redis")
        return result

    async def set(self, key: str, value: str) -> None:
        self.redis.set(key, value)
