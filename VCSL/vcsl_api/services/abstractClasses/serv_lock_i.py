from abc import ABC, abstractmethod


class ILockService(ABC):
    @abstractmethod
    async def acquire_lock(self, lock_name: str, acquire_timeout: int = 10, blocking: bool = True) -> bool:
        ...

    @abstractmethod
    async def release_lock(self, lock_name: str) -> None:
        ...
