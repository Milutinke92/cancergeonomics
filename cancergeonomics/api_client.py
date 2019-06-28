from cancergeonomics.http.client import CGCBaseHttpClient
from cancergeonomics.resources.file import FileResource
from cancergeonomics.resources.project import ProjectResource


class ApiClient(CGCBaseHttpClient):
    project = ProjectResource
    file = FileResource

    def __init__(self, token, api='https://cgc-api.sbgenomics.com/v2/', timeout=30):
        super(ApiClient, self).__init__(token, api, timeout)
