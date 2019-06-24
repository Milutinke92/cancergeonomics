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
@click.pass_context
def list(ctx):
    project_handler = ctx.obj['project_handler']
    for project in project_handler.list():
        click.echo(project)


@click.group()
@click.pass_context
def files(ctx):
    ctx.obj['file_handler'] = FileResource(api_client=ctx.obj['api_client'])

@files.command()
@click.option('--project', 'project_id', required=True)
@click.pass_context
def list(ctx, project_id):
    file_handler = ctx.obj['file_handler']
    for file in file_handler.list(query_params={"project": project_id}):
        click.echo(file)


@files.command()
@click.option('--file', 'file_id', required=True)
@click.pass_context
def stat(ctx, file_id):
    file_handler = ctx.obj['file_handler']
    click.echo(file_handler.stat(file_id))

@files.command()
@click.option('--file', 'file_id', required=True)
@click.argument('update_fields', nargs=-1, required=False, callback=validate_parameters)
@click.pass_context
def update(ctx, file_id, update_fields):
    file_handler = ctx.obj['file_handler']
    file_handler.update(file_id, data=update_fields)

@files.command()
@click.option('--file', 'file_id', required=True)
def download(file_id):
    pass


cgccli.add_command(projects)
cgccli.add_command(files)
