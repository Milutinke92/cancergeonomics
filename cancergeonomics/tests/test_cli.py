import pytest
from click.testing import CliRunner

from cancergeonomics import cli
from cancergeonomics.resources.project import ProjectResource


@pytest.fixture
def test_data():
    return ["test"]


@pytest.fixture
def project_list_action(mocker, test_data):
    """
    Purpose of this fixture is to mock `get_download_url` method of FileResource
    :param mocker: MockFixture instance
    :param get_download_url: pytest fixture get_download_url
    :return: mocked FileResource with get_download_url method
    """
    mocker.patch.object(ProjectResource, 'list', return_value=test_data)
    return mocker


def testr_project_list_command(project_list_action, test_data):
    runner = CliRunner()
    result = runner.invoke(cli.cgccli, ['--token', 'sadsad', 'projects', 'list'])
    assert result.output == test_data[0] + "\n"
