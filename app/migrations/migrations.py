import os

from alembic.command import upgrade, downgrade
from alembic.config import Config


def make_migrations():
    migrations_dir = os.path.dirname(os.path.realpath(__file__))
    # this assumes the alembic.ini is also contained in this same directory
    config_file = os.path.join(migrations_dir, "alembic.ini")

    alembic_config = Config(file_=config_file)
    alembic_config.set_main_option("script_location", migrations_dir)

    # upgrade the database to the latest revision
    upgrade(alembic_config, "head")


def clear_db():
    migrations_dir = os.path.dirname(os.path.realpath(__file__))
    # this assumes the alembic.ini is also contained in this same directory
    config_file = os.path.join(migrations_dir, "alembic.ini")

    alembic_config = Config(file_=config_file)
    alembic_config.set_main_option("script_location", migrations_dir)

    # upgrade the database to the latest revision
    downgrade(alembic_config, 'base')
