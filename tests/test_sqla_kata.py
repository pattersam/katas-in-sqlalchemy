import itertools
import os

import pytest
import sqlalchemy as sa
from sqla_kata import commands, db_engine, run, variations

IN_MEMORY_SQLITE_DB_CONNECTION_STRING = "sqlite://"


@pytest.fixture
def test_db_connection_string() -> str:
    os.environ["SQLA_KATA_DB_CONN_STRING"] = IN_MEMORY_SQLITE_DB_CONNECTION_STRING
    return IN_MEMORY_SQLITE_DB_CONNECTION_STRING


@pytest.fixture
def test_db_engine(test_db_connection_string: str) -> sa.Engine:
    """Returns an SQLAlchemy Engine, pointing to the in-memory sqlite db"""
    return db_engine.get_engine(db_connection_string=test_db_connection_string)


def test_completeness():
    for version_name, command_name in itertools.product(
        variations.VARIATIONS, commands.COMMANDS
    ):
        version_module = getattr(variations, version_name)
        command_callable = getattr(version_module, command_name)
        assert callable(command_callable)


def test_run_all() -> None:
    run.run_all()


@pytest.mark.parametrize("variation", variations.VARIATIONS)
def test_command_create_tables(
    variation: variations.Variation, test_db_engine: sa.Engine
):
    run.run_one(variation, "create_tables", test_db_engine)
    with test_db_engine.connect() as conn:
        actual = (
            conn.execute(sa.text("SELECT name FROM sqlite_master WHERE type='table';"))
            .scalars()
            .all()
        )
    assert len(actual) == 3
    assert set(actual) == {"users", "tools", "bookings"}
