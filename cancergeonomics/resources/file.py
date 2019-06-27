from cancergeonomics.resources.meta.base import Resource


class FileResource(Resource):
    RESOURCE_ROOT_URL = "files"

    @classmethod
    def list(cls, project_id, **kwargs):
        """
        Get the list of Files for related to project
        :param project: id of the project for which we want list of files
        :param kwargs: query params
        :return: list of Files items related to project
        """
        return cls.filter(project=project_id, **kwargs)

    @classmethod
    def stat(cls, file_id, **kwargs):
        """
        Get the list of Files for related to project
        :param file_id: id of the File for which we download url
        :param kwargs: query params
        :return: get file details
        """
        return cls.get(file_id, **kwargs)

    @classmethod
    def download(cls, file_id, file_path, **kwargs):
        """
        Get the list of Files for related to project
        :param file_id: id of the File for which we download url
        :param file_path: path to which downloaded file will be stored
        :param kwargs: query params
        :return: file path where file is stored
        """
        url = cls.get_download_url(file_id)
        return cls.api_client.download(url, file_path, query_params=kwargs)

    @classmethod
    def get_download_url(cls, file_id):
        """
        Get the list of Files for related to project
        :param file_id: id of the File for which we download url
        :return: Url from which file can be downloaded
        """
        data = cls.api_client.get('files/{}/download_info'.format(file_id))
        return data['url']
