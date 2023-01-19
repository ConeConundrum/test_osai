import hashlib
import base64
import random
from typing import Optional

from asyncpg import Pool
from pydantic import HttpUrl

from app.settings.config import config
from app.database.crud_operations import get_key_db


async def check_collision(db: Pool, key: str) -> bool:
    collision = await get_key_db(db=db, key=key)
    return bool(collision)


async def generate_key(db: Pool, original_url: HttpUrl, salt: Optional[str] = None) -> Optional[str]:
    """Function generating short key for url creation based on md5 hash"""
    # add salt if previous key has collision
    key: Optional[str] = None
    retry_counter: int = 50

    while not key and retry_counter > 0:
        hashable_string = original_url.encode('utf-8') if not salt else ''.join([original_url, salt]).encode('utf-8')

        # hashing, make url safe and get only 8 chars from hash
        key_bytes: bytes = hashlib.md5(hashable_string).digest()  # nosec just hashing to get random string
        key: str = base64.urlsafe_b64encode(key_bytes).decode('ascii')[:config.MAX_KEY_LENGTH]

        # check for collision and add salt from random
        if await check_collision(db=db, key=key):
            salt = str(random.randint(1, 1000000))
        retry_counter -= 1

    return key


def generate_short_url(original_url: HttpUrl, key: str) -> str:
    short_url = ''.join([original_url.host, '/', key])
    return short_url
