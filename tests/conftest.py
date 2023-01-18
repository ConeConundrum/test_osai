import asyncio
import pytest
from asyncpg import Pool
from fastapi.testclient import TestClient

from app.db.database import get_connection_pool, initiate_db, make_migrations, clear_db


@pytest.fixture(scope='session')
def manage_db():
    asyncio.get_event_loop().run_until_complete(initiate_db())
    # make_migrations()
    yield
    # clear_db()


@pytest.fixture(scope='session')
def manage_db_connection_pool(manage_db) -> Pool:
    connection_pool: Pool = asyncio.get_event_loop().run_until_complete(get_connection_pool())
    yield connection_pool
    asyncio.get_event_loop().run_until_complete(connection_pool.close())


@pytest.fixture(scope='module')
def client(manage_db):
    from app.main import app
    with TestClient(app) as client:
        yield client
