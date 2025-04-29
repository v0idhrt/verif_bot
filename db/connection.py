import asyncpg
from config import settings  # предполагаем, что ты хранишь creds в .env

class DB:
    pool: asyncpg.Pool = None

    @classmethod
    async def connect(cls):
        cls.pool = await asyncpg.create_pool(
            dsn=settings.database_url  # например: postgres://user:pass@localhost/dbname
        )

    @classmethod
    async def close(cls):
        await cls.pool.close()
