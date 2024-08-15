# katas-in-sqlalchemy

Coding Katas that use SQLAlchemy in different ways

## Concept

This project demonstrates multiple _variations_ of different ways to use
SQLAlchemy to implement various database _commands_ 

* Variations - each of these is a different implementation of the commands
* Commands - actions performed on the database (e.g. querying, inserting, etc.)

## CLI Usage

Run a single variation's command with:

```bash
hatch run sqla-kata run {version} {command}
```

For example, to create tables with using plain SQL operations with SQLAlchemy,
run:

```bash
hatch run sqla-kata run v1_sql create_tables
```

Or run all of the versions and commands with:

```bash
hatch run sqla-kata all
```

## Development guide

### Running tests

```bash
hatch run pytest
```

### Add a new version

🚧 TODO

### Add a new command

🚧 TODO

## Pre-requisites

* Python 3.12 (e.g. with `pyenv install 3.12`)
* [Hatch](https://hatch.pypa.io/latest/) (e.g. with `pipx install hatch`)
