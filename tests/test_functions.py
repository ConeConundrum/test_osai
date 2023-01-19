import asyncio

from app.components.generate_url import generate_short_url, generate_key, check_collision


def test_check_collision_positive_collision(db_pool, create_url_record_db):
    _, key, __, ___ = create_url_record_db

    collision = asyncio.get_event_loop().run_until_complete(
        check_collision(db=db_pool, key=key)
    )
    assert collision


def test_check_collision_no_collision(db_pool, create_url_record_data):
    _, key, __ = create_url_record_data

    collision = asyncio.get_event_loop().run_until_complete(
        check_collision(db=db_pool, key=key)
    )
    assert not collision


def test_generate_key_positive(db_pool, create_url_record_data):
    original_url, _, __ = create_url_record_data
    generated_key = asyncio.get_event_loop().run_until_complete(
        generate_key(db=db_pool, original_url=original_url)
    )
    assert generated_key


def test_generate_short_url_positive(create_url):
    assert generate_short_url(original_url=create_url, key='key')
