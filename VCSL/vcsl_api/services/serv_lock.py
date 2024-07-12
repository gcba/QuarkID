from services.abstractClasses.serv_lock_i import ILockService
from kink import inject
from redis import Redis
from time import time
from asyncio import sleep


@inject(alias=ILockService)
class LockService(ILockService):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def acquire_lock(self, lock_name: str, acquire_timeout: int = 10, blocking: bool = True) -> bool:
        lock_name = f"lock:{lock_name}"
        acquire = None
        t = time()  # time in seconds
        while acquire is None and blocking:
            acquire = self.redis.set(lock_name, 1, nx=True, ex=acquire_timeout)
            if (time() - t) > acquire_timeout:
                break
            await sleep(0)  # Give up control to other tasks
        return acquire

    async def release_lock(self, lock_name: str) -> None:
        lock_name = f"lock:{lock_name}"
        self.redis.delete(lock_name)
