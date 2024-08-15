import os

import sqlalchemy as sa

from sqla_kata import logging


def get_db_connection_string(default_sqlite_filename: str = "sqlite") -> str:
    return os.getenv(
        "SQLA_KATA_DB_CONN_STRING", f"sqlite:///{default_sqlite_filename}.db"
    )


def get_engine(
    db_connection_string: str | None = None, engine_logging: bool = False
) -> sa.Engine:
    if db_connection_string is None:
        db_connection_string = get_db_connection_string()
    if engine_logging:
        logging.configure_sqla_engine_logging()
    return sa.create_engine(db_connection_string, echo=engine_logging)
