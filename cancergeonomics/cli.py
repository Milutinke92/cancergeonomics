import click

from cancergeonomics.api_client import ApiClient
from cancergeonomics.helpers import unflatten


def validate_parameters(ctx, param, value, flatten=False):
    """
    This function is taking values provided for some argument or option
    checks if format {field name}={value} is valid and returns flatten data
    Example: metada.simple_id=test returns {"metadata": {"simple_id": "test"}}
    :param ctx: Context instance
    :param param: Option instance
    :param value: provided values
    :return:
    """
    try:
        data = dict([k.split('=') for k in value])
        if flatten:
            return unflatten(data)
        return data
    except ValueError:
        raise click.BadParameter('rolls need to be in format N=v')


def validate_parameters_flatten(ctx, param, value):
    return validate_parameters(ctx, param, value, flatten=True)


query_params_option = click.option(
    '--query_params', '-qp', multiple=True, required=False,
    callback=validate_parameters,
    help="Request query params in {field name}={value} format. For nested fields use "
         "{field_name}.{nested field name}={value} format"
)


@click.group()
@click.option('--token', type=click.STRING, required=True, help="Token for authorization on API")
@click.pass_context
def cgccli(ctx, token):
    """
    Main command
    :param ctx: Context instance
    :param token: Authorization token
    :return:
    """
    ctx.obj = dict()
    ctx.obj['api_client'] = ApiClient(token=token)


@click.group()
@click.pass_context
def projects(ctx):
    """
    ExecuteProjectResource related commands.
    """
    pass


@projects.command(name='list')
@query_params_option
@click.pass_context
def list_command(ctx, query_params):
    """
    Executing and displaying results of ProjectResource.list method
    :param ctx: Context instance
    :param query_params: dictionary of fields and values which will be used for request query params
    """
    api_client = ctx.obj['api_client']
    for project in api_client.project.list(**query_params):
        click.echo(project)


@click.group()
@click.pass_context
def files(ctx):
    """
    ExecuteFileResource related commands.
    """
    pass


@files.command(name='list')
@click.option('--project', 'project_id', required=True)
@query_params_option
@click.pass_context
def list(ctx, project_id, query_params):
    """
    Executing and displaying results of FileResource.list method
    :param ctx: Context instance
    :param query_params: dictionary of fields and values which will be used for request query params
    """
    api_client = ctx.obj['api_client']
    for file in api_client.file.list(project_id, **query_params):
        click.echo(file)


@files.command()
@click.option('--file', 'file_id', required=True)
@query_params_option
@click.pass_context
def stat(ctx, file_id, query_params):
    """
    Executing and displaying results of FileResource.stat method
    :param ctx: Context instance
    :param query_params: dictionary of fields and values which will be used for request query params
    """
    api_client = ctx.obj['api_client']
    click.echo(api_client.file.stat(file_id, **query_params))


@files.command()
@click.option('--file', 'file_id', required=True)
@click.argument('update_fields', nargs=-1, required=True, callback=validate_parameters)
@click.option(
    '--query_params', '-qp', multiple=True, required=False, callback=validate_parameters_flatten,
    help="Request query params in {field name}={value} format. "
         "For nested fields use {field_name}.{nested field name}={value} format"
)
@click.pass_context
def update(ctx, file_id, update_fields, query_params):
    """
    Executing and displaying results of FileResource.update method
    :param ctx: Context instance
    :param query_params: dictionary of fields and values which will be used for request query params
    """
    api_client = ctx.obj['api_client']
    click.echo(api_client.file.update(file_id, data=update_fields, **query_params))


@files.command()
@click.pass_context
@click.option('--file', 'file_id', required=True)
@click.option('--dst', 'dst', required=True, type=click.Path())
@query_params_option
def download(ctx, file_id, dst, query_params):
    """
    Executing and displaying results of FileResource.download.
    :param ctx: Context instance
    :param query_params: dictionary of fields and values which will be used for request query params
    """
    api_client = ctx.obj['api_client']
    file_path = api_client.file.download(file_id, dst, **query_params)
    click.echo(file_path)


cgccli.add_command(projects)
cgccli.add_command(files)
