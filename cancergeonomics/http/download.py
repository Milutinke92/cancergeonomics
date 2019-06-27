import os

import requests

from cancergeonomics.http.exceptions import FileDownloadException


class Download(object):
    """
    Handling Downloads of Resources
    """

    def __init__(self, url, file_path, stream=True, chunk_size=8192, query_params=None):
        super(Download, self).__init__()
        self.url = url
        self.file_path = file_path
        self.stream = stream
        self.chunk_size = chunk_size
        self.query_params = query_params

    def is_downloadable(self, headers):
        """
        Does the url contain a downloadable resource
        :param: HTTP Response Headers
        :return boolean:
        """
        content_type = headers.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False

        return True

    def download(self):
        """
        Method for downloading and storing data on disk with given file_path
        :return: file_path where file is stored
        """

        file_path = self.file_path

        if os.path.isdir(file_path):
            local_filename = self.url.split('/')[-1]
            file_path = os.path.join(file_path, local_filename)

        res_head = requests.head(self.url)

        if not self.is_downloadable(res_head.headers):
            raise FileDownloadException(
                "Provided URL {} doesn't containt downloadable content".format(self.url)
            )

        res = requests.get(self.url, params=self.query_params)
        with open(file_path, 'wb') as file_:
            file_.write(res.content)

        return file_path
