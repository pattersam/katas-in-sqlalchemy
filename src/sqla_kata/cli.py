import typing as t

import click

from sqla_kata import versions

Commands = t.Literal["create_tables"]

class Interface(t.Protocol):
    """
    Taking advantage of the fact that protocols also work for modules.
    """
    def create_tables(self): ...

@click.command()
@click.argument("version", type=click.Choice(t.get_args(versions.Versions)))
@click.argument("command", type=click.Choice(t.get_args(Commands)))
def sqla_kata(version: versions.Versions, command: Commands):
    # resolve selected version
    match version:
        case "v1_sql":
            kata_version = versions.v1_sql
        case _:
            t.assert_never(version)

    # resolve selected command
    match command:
        case "create_tables":
            kata_version.create_tables()
        case _:
            t.assert_never(command)
