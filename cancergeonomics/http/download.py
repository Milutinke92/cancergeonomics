import os

import requests

from cancergeonomics.http.exceptions import FileDownloadExceptioon


class Download(object):

    def __init__(self, url, file_path, stream=True, chunk_size=8192):
        self.url = url
        self.file_path = file_path
        self.stream = stream
        self.chunk_size = chunk_size

    def is_downloadable(self):
        """
        Does the url contain a downloadable resource
        """
        h = requests.head(self.url)
        header = h.headers
        content_type = header.get('content-type')
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        return True

    def download(self, file_path=None):

        file_path = file_path if file_path else self.file_path

        if os.path.isdir(file_path):
            local_filename = self.url.split('/')[-1]
            file_path = os.path.join(file_path, local_filename)

        if self.stream:
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            f.write(chunk)
        else:
            requests.get(self.url)

        return file_path

    def run_download(self, file_path=None):
        if not self.is_downloadable():
            raise FileDownloadExceptioon

        return self.download(file_path)
