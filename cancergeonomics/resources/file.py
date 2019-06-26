from cancergeonomics.resources.meta.base import Resource


class FileResource(Resource):
    RESOURCE_ROOT_URL = "files"

    @classmethod
    def list(cls, project, **kwargs):
        return cls.filter(project=project, **kwargs)

    @classmethod
    def stat(cls, file_id, **kwargs):
        return cls.get(file_id, **kwargs)

    @classmethod
    def download(cls, file_id, file_path, **kwargs):
        url = cls.get_download_url(file_id)
        return cls.api_client.download(url, file_path, query_params=kwargs)

    @classmethod
    def get_download_url(cls, file_id):
        data = cls.api_client.get(f'files/{file_id}/download_info')
        return data['url']
