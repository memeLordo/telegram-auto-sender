import asyncio
from asyncio import Lock


class SingletonAsync:
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(SingletonAsync, cls).__new__(cls)
            return cls._instance

    async def __call__(self, *args, **kwargs) -> bool:
        if not hasattr(self, "_is_called"):
            self._is_called: bool = True
            # Ваше асинхронное действие здесь
            await self._async_action(*args, **kwargs)
            return self._is_called
        else:
            return False

    async def _async_action(self, *args, **kwargs):
        # Ваше асинхронное действие здесь
        await asyncio.sleep(2)  # Пример асинхронной задержки


class BanHandler(metaclass=SingletonAsync):

    async def _async_action(self, *clients, **_):
        # Ваше асинхронное действие здесь
        for client in clients:
            await client.send
        await asyncio.sleep(2)  # Пример асинхронной задержки
