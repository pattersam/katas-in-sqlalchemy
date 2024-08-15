import click

from sqla_kata import commands, run, variations


@click.group()
def sqla_kata(): ...


@sqla_kata.command(name="run")
@click.argument("variation", type=click.Choice(variations.VARIATIONS))
@click.argument("command", type=click.Choice(commands.COMMANDS))
def _(variation: variations.Variation, command: commands.Command):
    run.run_one(variation, command)


@sqla_kata.command()
def all():
    run.run_all()


@sqla_kata.command()
@click.argument("variation", type=click.Choice(variations.VARIATIONS))
def report(variation: variations.Variation):
    run.report(variation)


@sqla_kata.command()
def clean():
    run.clean_all()
