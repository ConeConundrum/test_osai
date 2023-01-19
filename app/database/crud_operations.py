from asyncpg import Pool
from pydantic import HttpUrl


async def create_url_db(db: Pool, original_url: HttpUrl, short_url: str, generated_key: str) -> str:
    async with db.acquire() as connection:
        return await connection.fetchval(
            """
            INSERT INTO url (
                original_url,
                short_url,
                key
            ) VALUES ($1, $2, $3)
            ON CONFLICT DO NOTHING
            RETURNING short_url;
            """,
            original_url,
            short_url,
            generated_key
        )


async def get_short_url_db(db: Pool, key: str) -> HttpUrl:
    async with db.acquire() as connection:
        return await connection.fetchval(
            """
            SELECT original_url FROM url
            WHERE key = $1
            """,
            key
        )


async def get_full_url_db(db: Pool, original_url: HttpUrl) -> HttpUrl:
    async with db.acquire() as connection:
        return await connection.fetchval(
            """
            SELECT short_url FROM url
            WHERE original_url = $1
            """,
            original_url
        )


async def get_key_db(db: Pool, key: str) -> str:
    async with db.acquire() as connection:
        return await connection.fetchval(
            """
            SELECT key FROM url
            WHERE key = $1
            """,
            key
        )


async def delete_url_db(db: Pool, key: str) -> None:
    async with db.acquire() as connection:
        return await connection.fetchval(
            """
            DELETE FROM url
            WHERE key = $1
            RETURNING original_url
            """,
            key
        )
