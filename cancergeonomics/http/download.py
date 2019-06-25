import os

import requests

from cancergeonomics.http.exceptions import FileDownloadException


class Download(object):
    """
    Handling Downloads of Resources
    """

    def __init__(self, url, file_path, stream=True, chunk_size=8192):
        self.url = url
        self.file_path = file_path
        self.stream = stream
        self.chunk_size = chunk_size

    def is_downloadable(self):
        """
        Does the url contain a downloadable resource
        :return boolean:
        """
        res_head = requests.head(self.url)
        header = res_head.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    def download(self, file_path=None):
        """
        Method for downloading and storing data on disk with given file_path
        :param file_path:
        :return file_path as string:
        """

        file_path = file_path if file_path else self.file_path

        if os.path.isdir(file_path):
            local_filename = self.url.split('/')[-1]
            file_path = os.path.join(file_path, local_filename)

        if self.stream:
            with requests.get(self.url, stream=True) as res:
                res.raise_for_status()
                with open(file_path, 'wb') as file_:
                    for chunk in res.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            file_.write(chunk)
        else:
            requests.get(self.url)

        return file_path

    def run_download(self, file_path=None):
        """
        Method for checking if Content is downlodable and runing actual download
        :param file_path:
        :return file_path as string:
        """
        if not self.is_downloadable():
            raise FileDownloadException(
                "Provided URL {} doesn't containt downloadable content".format(self.url)
            )

        return self.download(file_path)
