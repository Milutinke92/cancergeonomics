from cancergeonomics.http.client import CGCBaseHttpClient
from cancergeonomics.resources.file import FileResource
from cancergeonomics.resources.project import ProjectResource


class ApiClient(CGCBaseHttpClient):
    project = ProjectResource
    file = FileResource
