from abc import ABC, abstractmethod


class ICacheService(ABC):
    @abstractmethod
    async def get(self, key: str) -> str:
        ...

    async def set(self, key: str, value: str) -> None:
        ...
