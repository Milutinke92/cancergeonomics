import click

from cancergeonomics.helpers import unflatten
from cancergeonomics.http.client import CGCBaseHttpClient
from cancergeonomics.resources.file import FileResource
from cancergeonomics.resources.project import ProjectResource


def validate_parameters(ctx, param, value):
    try:
        data = dict([k.split('=') for k in value])
        return unflatten(data)
    except ValueError:
        raise click.BadParameter('rolls need to be in format NdM')

@click.group()
@click.option('--token', type=click.STRING, required=True)
@click.pass_context
def cgccli(ctx, token):
    ctx.obj = {}
    ctx.obj['api_client'] = CGCBaseHttpClient(token=token)


@click.group()
@click.pass_context
def projects(ctx):
    ctx.obj['project_handler'] = ProjectResource(api_client=ctx.obj['api_client'])


@projects.command()
@click.option('--limit', 'limit', required=False, type=click.IntRange(min=1, max=100), default=25)
@click.option('--offset', 'offset', required=False, type=click.IntRange(min=0, max=None), default=0)
@click.option('--name', 'name', required=False, type=str)
@click.option('--fields', 'fields', required=False, default='_all')
@click.pass_context
def list(ctx, **query_params):
    query_params = {k: v for k, v in query_params.items() if v is not None}
    project_handler = ctx.obj['project_handler']
    for project in project_handler.list(query_params=query_params):
        click.echo(project)


@click.group()
@click.pass_context
def files(ctx):
    ctx.obj['file_handler'] = FileResource(api_client=ctx.obj['api_client'])

@files.command()
@click.option('--project', 'project', required=True)
@click.pass_context
def list(ctx, **kwargs):
    file_handler = ctx.obj['file_handler']
    for file in file_handler.list(query_params=kwargs):
        click.echo(file)


@files.command()
@click.option('--file', 'file_id', required=True)
@click.pass_context
def stat(ctx, file_id):
    file_handler = ctx.obj['file_handler']
    click.echo(file_handler.stat(file_id))

@files.command()
@click.option('--file', 'file_id', required=True)
@click.argument('update_fields', nargs=1, required=False, callback=validate_parameters)
@click.pass_context
def update(ctx, file_id, update_fields):
    file_handler = ctx.obj['file_handler']
    file_handler.update(file_id, data=update_fields)

@files.command()
@click.pass_context
@click.option('--file', 'file_id', required=True)
@click.option('--dst', 'dst', required=True, type=click.Path())
def download(ctx, file_id, dst):
    file_handler = ctx.obj['file_handler']
    file_path = file_handler.download(file_id, dst)
    click.echo(file_path)

cgccli.add_command(projects)
cgccli.add_command(files)
