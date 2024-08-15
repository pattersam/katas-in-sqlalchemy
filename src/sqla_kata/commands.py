import typing as t

Command = t.Literal["create_tables", "save_bookings", "get_bookings"]

COMMANDS: tuple[Command] = t.get_args(Command)

RUN_ALL_COMMAND_SEQUENCE: list[Command] = [
    "create_tables",
    "save_bookings",
    "get_bookings",
]
