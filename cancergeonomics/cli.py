import click

from cancergeonomics.api_client import ApiClient
from cancergeonomics.helpers import unflatten


def validate_parameters(ctx, param, value):
    try:
        data = dict([k.split('=') for k in value])
        return unflatten(data)
    except ValueError:
        raise click.BadParameter('rolls need to be in format N=v')


@click.group()
@click.option('--token', type=click.STRING, required=True)
@click.pass_context
def cgccli(ctx, token):
    ctx.obj = {}
    ctx.obj['api_client'] = ApiClient(token=token)


@click.group()
@click.pass_context
def projects(ctx):
    pass


@projects.command()
@click.option('--query_params', '-qp', multiple=True, required=False, callback=validate_parameters)
@click.pass_context
def list(ctx, query_params):
    api_client = ctx.obj['api_client']
    for project in api_client.project.list(**query_params):
        click.echo(project)


@click.group()
@click.pass_context
def files(ctx):
    pass


@files.command()
@click.option('--project', 'project', required=True)
@click.option('--query_params', '-qp', multiple=True, required=False, callback=validate_parameters)
@click.pass_context
def list(ctx, project, query_params):
    api_client = ctx.obj['api_client']
    for file in api_client.file.list(project, **query_params):
        click.echo(file)


@files.command()
@click.option('--file', 'file_id', required=True)
@click.option('--query_params', '-qp', multiple=True, required=False, callback=validate_parameters)
@click.pass_context
def stat(ctx, file_id, query_params):
    api_client = ctx.obj['api_client']
    click.echo(api_client.file.stat(file_id, **query_params))


@files.command()
@click.option('--file', 'file_id', required=True)
@click.argument('update_fields', nargs=-1, required=True, callback=validate_parameters)
@click.option('--query_params', '-qp', multiple=True, required=False, callback=validate_parameters)
@click.pass_context
def update(ctx, file_id, update_fields, query_params):
    api_client = ctx.obj['api_client']
    click.echo(api_client.file.update(file_id, data=update_fields, **query_params))


@files.command()
@click.pass_context
@click.option('--file', 'file_id', required=True)
@click.option('--dst', 'dst', required=True, type=click.Path())
@click.option('--query_params', '-qp', multiple=True, required=False, callback=validate_parameters)
def download(ctx, file_id, dst, query_params):
    api_client = ctx.obj['api_client']
    file_path = api_client.file.download(file_id, dst, **query_params)
    click.echo(file_path)


cgccli.add_command(projects)
cgccli.add_command(files)
