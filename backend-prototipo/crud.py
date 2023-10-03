import os

from asyncpg import Connection, create_pool
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ADDRESS = "localhost"

url_admins = f"postgresql://postgres:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}"


async def get_session():
    async with create_pool(url_admins) as pool:
        async with pool.acquire() as con:
            yield con


async def get_transcripcion(id: str, conn: Connection) -> tuple[str, str]:
    query = f"SELECT * FROM transcripciones_video WHERE video_id = '{id}';"
    result = await conn.fetchrow(query)
    if (
        result is None
        or result["transcripcion"] is None
        or result["video_descripcion"] is None
    ):
        raise HTTPException(status_code=404, detail="Transcripcion not found")
    return (result["transcripcion"], result["video_descripcion"])
