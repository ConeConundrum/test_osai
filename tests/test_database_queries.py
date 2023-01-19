import asyncio

from app.database.crud_operations import create_url_db, get_short_url_db, delete_url_db, get_full_url_db, get_key_db


def test_create_url_db_ok(db_pool, create_url_record_data):
    original_url, key, short_url = create_url_record_data
    created = asyncio.get_event_loop().run_until_complete(
        create_url_db(
            db=db_pool,
            original_url=original_url,
            generated_key=key,
            short_url=short_url
        )
    )

    assert created
    assert created == short_url


def test_create_url_db_conflict(db_pool, create_url_record_db):
    original_url, key, short_url, _ = create_url_record_db

    created = asyncio.get_event_loop().run_until_complete(
        create_url_db(
            db=db_pool,
            original_url=original_url,
            generated_key=key,
            short_url=short_url
        )
    )
    assert not created


def test_get_url_db_ok(db_pool, create_url_record_db):
    original_url, key, _, __ = create_url_record_db

    record = asyncio.get_event_loop().run_until_complete(
        get_short_url_db(
            db=db_pool,
            key=key
        )
    )

    assert record
    assert record == original_url


def test_get_url_no_record(db_pool, create_url_record_data):
    _, key, _ = create_url_record_data

    record = asyncio.get_event_loop().run_until_complete(
        get_short_url_db(
            db=db_pool,
            key=key
        )
    )

    assert not record


def test_delete_url_db_ok(db_pool, create_url_record_db):
    original_url, key, _, __ = create_url_record_db

    record = asyncio.get_event_loop().run_until_complete(
        delete_url_db(
            db=db_pool,
            key=key
        )
    )

    assert record
    assert record == original_url


def test_delete_url_no_record(db_pool, create_url_record_data):
    _, key, __ = create_url_record_data

    record = asyncio.get_event_loop().run_until_complete(
        get_short_url_db(
            db=db_pool,
            key=key
        )
    )

    assert not record


def test_get_full_url_db_ok(db_pool, create_url_record_db):
    original_url, _, short_url, __ = create_url_record_db

    record = asyncio.get_event_loop().run_until_complete(
        get_full_url_db(
            db=db_pool,
            original_url=original_url
        )
    )

    assert record
    assert record == short_url


def test_get_full_url_db_no_record(db_pool, create_url_record_data):
    original_url, _, __ = create_url_record_data

    record = asyncio.get_event_loop().run_until_complete(
        get_full_url_db(
            db=db_pool,
            original_url=original_url
        )
    )

    assert not record


def test_get_key_db_ok(db_pool, create_url_record_db):
    _, key, __, ___ = create_url_record_db

    record = asyncio.get_event_loop().run_until_complete(
        get_key_db(
            db=db_pool,
            key=key
        )
    )

    assert record
    assert record == key


def test_get_key_db_no_record(db_pool, create_url_record_data):
    _, key, __ = create_url_record_data

    record = asyncio.get_event_loop().run_until_complete(
        get_key_db(
            db=db_pool,
            key=key
        )
    )

    assert not record
