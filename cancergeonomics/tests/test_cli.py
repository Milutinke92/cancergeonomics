import pytest
from click.testing import CliRunner

from cancergeonomics import cli
from cancergeonomics.resources.file import FileResource
from cancergeonomics.resources.project import ProjectResource


@pytest.fixture
def test_data():
    """
    Test data fixture
    :return: list
    """
    return ["test"]


@pytest.fixture
def project_resource(mocker, test_data):
    """
    FileResource fixture with mocked methods: list, stat, update, download
    :param mocker: MockFixture instance
    :param test_data: pytest fixture data which will be returned on FileResource mocked methods
    :return: pytest MockFixture
    """
    mocker.patch.object(ProjectResource, 'list', return_value=test_data)
    return mocker


@pytest.fixture
def file_resource(mocker, test_data):
    """
    FileResource fixture with mocked methods: list, stat, update, download
    :param mocker: MockFixture instance
    :param test_data: pytest fixture data which will be returned on FileResource mocked methods
    :return: pytest MockFixture
    """
    mocker.patch.object(FileResource, 'list', return_value=test_data)
    mocker.patch.object(FileResource, 'stat', return_value=test_data)
    mocker.patch.object(FileResource, 'update', return_value=test_data)
    mocker.patch.object(FileResource, 'download', return_value=test_data)
    return mocker


def test_project_list_command(project_resource, test_data):
    """
    Test Command Client `project list` command
    :param file_resource: Mocked ProjectResource fixture
    :param test_data: test data fixture
    """
    runner = CliRunner()
    result = runner.invoke(cli.cgccli, ['--token', 'sadsad', 'projects', 'list'])
    assert result.output == test_data[0] + "\n"


def test_file_list_command(file_resource, test_data):
    """
    Test Command Client `files list` command
    :param file_resource: Mocked FileResource fixture
    :param test_data: test data fixture
    """
    runner = CliRunner()
    result = runner.invoke(cli.cgccli, ['--token', 'sadsad', 'files', 'list', '--project', 'test'])
    assert result.output == test_data[0] + "\n"


def test_file_stat_command(file_resource, test_data):
    """
    Test Command Client `files stat` command
    :param file_resource: Mocked FileResource fixture
    :param test_data: test data fixture
    """
    runner = CliRunner()
    result = runner.invoke(cli.cgccli, ['--token', 'sadsad', 'files', 'stat', '--file', 'test'])
    assert result.output == str(test_data) + "\n"


def test_file_update_command(file_resource, test_data):
    """
    Test Command Client `files update` command
    :param file_resource: Mocked FileResource fixture
    :param test_data: test data fixture
    """
    runner = CliRunner()
    result = runner.invoke(cli.cgccli, ['--token', 'sadsad', 'files', 'update', '--file', 'test', 'name=test'])
    assert result.output == str(test_data) + "\n"


def test_file_download_command(file_resource, test_data):
    """
    Test Command Client `files download` command
    :param file_resource: Mocked FileResource fixture
    :param test_data: test data fixture
    """
    runner = CliRunner()
    result = runner.invoke(
        cli.cgccli, ['--token', 'sadsad', 'files', 'download', '--file', 'test', '--dst', '/tmp/file']
    )
    assert result.output == str(test_data) + "\n"
