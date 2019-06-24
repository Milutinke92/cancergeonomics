import click
import sys

class Config(object):

    def __init__(self, token):
        self.token = token

pass_config = click.make_pass_decorator(Config)

@click.group()
@click.option('--token', type=click.STRING, required=True)
@click.pass_context
def cgccli(ctx, token):
    ctx.obj = Config(token=token)
    click.echo("test")


@click.group()
@click.pass_context
@pass_config
def projects(config, token):
    click.echo(config.token)
    click.echo("run projeccts")

@projects.command()
def list():
    click.echo("run list")


@click.group()
@click.pass_context
@pass_config
def files(config, token):
    click.echo(config.token)
    click.echo("run files")
    pass

@files.command()
@click.option('--file', 'file_id', required=True)
def stat(file_id):
    click.echo("run stat")
    click.echo(file_id)

@files.command()
@click.option('--file', 'file_id', required=True)
@click.argument()
def update(file_id):
    click.echo("run update")


@files.command()
@click.option('--file', 'file_id', required=True)
def download(file_id):
    click.echo("run download")
    click.echo("file_id")

cgccli.add_command(projects)
cgccli.add_command(files)
