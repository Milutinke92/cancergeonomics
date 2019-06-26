import json
import logging
import platform
from urllib.parse import urljoin

import pkg_resources
import requests

from cancergeonomics.http.download import Download
from cancergeonomics.http.error_handlers import handle_error_response
from cancergeonomics.http.exceptions import AuthTokenException

logger = logging.getLogger(__name__)

CLIENT_INFO = {
    'version': pkg_resources.get_distribution('cancergeonomics').version,
    'os': platform.system(),
    'python': platform.python_version(),
    'requests': requests.__version__,
}


class BaseSession(requests.Session):
    pass


class CGCBaseHttpClient(object):
    def __init__(self, token, api='https://cgc-api.sbgenomics.com/v2/', timeout=30):
        self.api = api
        self.token = token
        self.session = BaseSession()
        self.timeout = timeout
        self.headers = {
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent':
                'sevenbridges-python/{version} ({os}, Python/{python}; '
                'requests/{requests})'.format(**CLIENT_INFO)
        }

        if not self.token:
            raise AuthTokenException("Authentication token must be provided")

        self.headers.update({"X-SBG-Auth-Token": token})

    def _request(self, method, url, headers=None, params=None, data=None, append_url=True):
        if headers:
            headers.update(self.session.headers)
        else:
            headers = self.headers

        if append_url:
            url = urljoin(self.api, url)

        resp = self.session.request(
            method, url, headers=headers, params=params, data=json.dumps(data)
        )

        if not resp.ok:
            handle_error_response(resp)

        return resp.json()

    def get(self, url, headers=None, query_params=None, data=None, append_url=True):
        return self._request('GET', url, headers, query_params, data, append_url)

    def post(self, url, headers=None, query_params=None, data=None, append_url=True):
        return self._request('POST', url, headers, query_params, data, append_url)

    def put(self, url, headers=None, query_params=None, data=None, append_url=True):
        return self._request('PUT', url, headers, query_params, data, append_url)

    def patch(self, url, headers=None, query_params=None, data=None, append_url=True):
        return self._request('PATCH', url, headers, query_params, data, append_url)

    def delete(self, url, headers=None, query_params=None, data=None, append_url=True):
        return self._request('DELETE', url, headers, query_params, data, append_url)

    @staticmethod
    def download(url, file_path, stream=True, chunk_size=8192, query_params=None):
        logger.info("Download started to %s", file_path)
        download_obj = Download(url, file_path, stream, chunk_size, query_params=query_params)
        return download_obj.download()
