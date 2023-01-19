import asyncio
from typing import Tuple

import pytest
from asyncpg import Pool
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import HttpUrl, parse_obj_as

from app.database.crud_operations import create_url_db
from app.database.database import initiate_db, get_connection_pool
from app.components.generate_url import generate_key, generate_short_url
from app.migrations.migrations import make_migrations, clear_db

faker = Faker()


@pytest.fixture(scope='session')
def manage_db():
    """Database init for tests"""
    asyncio.get_event_loop().run_until_complete(initiate_db())
    make_migrations()
    yield
    clear_db()


@pytest.fixture(scope='session')
def db_pool(manage_db) -> Pool:
    """Init connection pool for functions using database"""
    connection_pool: Pool = asyncio.get_event_loop().run_until_complete(get_connection_pool())
    yield connection_pool
    asyncio.get_event_loop().run_until_complete(connection_pool.close())


@pytest.fixture(scope='module')
def client(manage_db):
    """Test app client"""
    from app.main import app
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='function')
def create_url(client) -> HttpUrl:
    """Single faked unique url"""
    return parse_obj_as(HttpUrl, faker.image_url())


@pytest.fixture(scope='function')
def create_url_record_data(db_pool) -> Tuple[HttpUrl, str, str]:
    """Full dataset for creation url record"""
    original_url = parse_obj_as(HttpUrl, faker.image_url())
    key = asyncio.get_event_loop().run_until_complete(
        generate_key(db=db_pool, original_url=original_url)
    )
    short_url = generate_short_url(original_url=original_url, key=key)

    return original_url, key, short_url


@pytest.fixture(scope='function')
def create_url_record_db(db_pool, create_url_record_data):
    """Full dataset with url record creation"""
    original_url, key, short_url = create_url_record_data
    created = asyncio.get_event_loop().run_until_complete(
        create_url_db(
            db=db_pool,
            original_url=original_url,
            generated_key=key,
            short_url=short_url
        )
    )
    assert created == short_url
    return original_url, key, short_url, created


@pytest.fixture(scope='function')
def create_url_record(client) -> Tuple[str, str]:
    """Url record created with api"""
    original_url = faker.image_url()
    result = client.post('/', params={'original_url': original_url})
    assert result.status_code == status.HTTP_201_CREATED
    return original_url, result.json()
