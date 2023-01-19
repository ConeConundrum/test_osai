import asyncio

import asyncpg
from fastapi import HTTPException, status
from alembic import command
from alembic.config import Config

from app.components.http_errors import HttpErrorEnum
from app.settings.config import config
from app.settings.logging import logger

alembic_config = Config('alembic.ini')


async def initiate_db():
    """Create db if not exist on startup and wait until successful connection"""

    logger.warning('Database initialization')
    connection = None
    while not connection:
        try:
            logger.warning(
                f'Try to connect to database '
                f'{config.POSTGRES_SERVER}, '
                f'{config.POSTGRES_PORT}, '
                f'{config.POSTGRES_DB}'
            )
            connection = await asyncpg.connect(
                user=config.POSTGRES_USER,
                database=config.POSTGRES_DB,
                password=config.POSTGRES_PASSWORD,
                port=config.POSTGRES_PORT,
                host=config.POSTGRES_SERVER
            )
        except asyncpg.InvalidCatalogNameError:
            logger.warning(
                f'Database {config.POSTGRES_DB} does not exist. '
                f'\n Creating database {config.POSTGRES_DB}'
            )
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
            return

        except (ConnectionRefusedError, asyncpg.CannotConnectNowError):
            logger.warning('Connection refused')

        except Exception as e:
            logger.error('Connection error', e)
        await asyncio.sleep(1)


def make_migrations():
    command.upgrade(alembic_config, 'head')


def clear_db():
    command.downgrade(alembic_config, 'base')


async def get_connection_pool():
    """Get connection pool with retries"""
    logger.warning('Database pool initialization')
    connection_pool = None
    while not connection_pool:
        try:
            connection_pool = await asyncpg.create_pool(
                host=config.POSTGRES_SERVER,
                port=config.POSTGRES_PORT,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                database=config.POSTGRES_DB,
                min_size=config.MIN_POOL_SIZE,
                max_size=config.MAX_POOL_SIZE,
            )
            logger.info("Database pool connection opened")

        except Exception as e:
            logger.error("Database pool connection opener error: ", e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=HttpErrorEnum.NO_DB_POOL_503
            )
        await asyncio.sleep(1)
    return connection_pool
