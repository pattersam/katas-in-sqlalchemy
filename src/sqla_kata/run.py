import functools
import itertools
import os
import typing as t

import rich.pretty
import sqlalchemy as sa

from sqla_kata import commands, db_engine, logging, variations


def _create_engine_for_variation(variation: variations.Variation) -> sa.Engine:
    return db_engine.get_engine(
        db_connection_string=db_engine.get_db_connection_string(variation),
        engine_logging=True,
    )


def run_one(
    variation: variations.Variation,
    command: commands.Command,
    engine: sa.Engine | None = None,
):
    logging.LOGGER.info('Using "%s" to run "%s"', variation, command)
    if engine is None:
        logging.LOGGER.info("Creating an SQLAlchemy engine for %s", variation)
        engine = _create_engine_for_variation(variation)

    # resolve selected variation
    match variation:
        case "v1_sql":
            variation_module = variations.v1_sql
        case "v2_core":
            variation_module = variations.v2_core
        case "v3_orm":
            variation_module = variations.v3_orm
        case _:
            t.assert_never(variation)

    # resolve selected command
    match command:
        case "create_tables":
            variation_module.create_tables(engine)
        case "save_bookings":
            variation_module.save_bookings(engine)
        case "get_bookings":
            variation_module.get_bookings(engine)
        case _:
            t.assert_never(command)


def run_all(engine: sa.Engine | None = None):
    list(
        itertools.starmap(
            functools.partial(run_one, engine=engine),
            itertools.product(variations.VARIATIONS, commands.RUN_ALL_COMMAND_SEQUENCE),
        )
    )


def report(variation: variations.Variation, engine: sa.Engine | None = None):
    if engine is None:
        engine = _create_engine_for_variation(variation)
    rich.pretty.pprint(getattr(variations, variation).get_bookings(engine))


def clean_all():
    for variation in variations.VARIATIONS:
        sqlite_file = f"{variation}.db"
        os.remove(sqlite_file) if os.path.exists(sqlite_file) else None
