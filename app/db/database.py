import asyncpg
from fastapi import HTTPException, status
from alembic import command
from alembic.config import Config

from app.settings import config
from app.settings.logging import logger

alembic_config = Config('alembic.ini')


async def initiate_db():
    logger.warning('Database initialization')
    try:
        logger.warning(
            f'Try to connect to database '
            f'{config.POSTGRES_SERVER}, '
            f'{config.POSTGRES_PORT}, '
            f'{config.POSTGRES_DB}'
        )
        await asyncpg.connect(
            user=config.POSTGRES_USER,
            database=config.POSTGRES_DB,
            password=config.POSTGRES_PASSWORD,
            port=config.POSTGRES_PORT,
            host=config.POSTGRES_SERVER
        )
    except asyncpg.InvalidCatalogNameError:
        logger.warning(f'Database {config.POSTGRES_DB} does not exist. \n Creating database {config.POSTGRES_DB}')
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            user=config.POSTGRES_USER,
            host=config.POSTGRES_SERVER,
            port=config.POSTGRES_PORT,
            password=config.POSTGRES_PASSWORD
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{config.POSTGRES_DB}" OWNER "{config.POSTGRES_USER}"'
        )
        await sys_conn.close()
        logger.info(f'Successfully create database {config.POSTGRES_DB}')


def make_migrations():
    command.upgrade(alembic_config, 'head')


def clear_db():
    command.downgrade(alembic_config, 'base')


async def get_connection_pool():
    logger.warning('Database pool initialization')
    try:
        _connection_pool = await asyncpg.create_pool(
            min_size=2,
            max_size=5,
            command_timeout=60,
            host=config.POSTGRES_SERVER,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database=config.POSTGRES_DB,
            # ssl="require",
        )
        logger.info("Database pool connection opened")
        return _connection_pool

    except Exception as e:
        logger.error("Database pool connection opener error: ", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database pool connection opener error"
        )
