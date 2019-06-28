import json
import logging
import platform
import sys

import requests

import cancergeonomics
from cancergeonomics.http.download import Download
from cancergeonomics.http.error_handlers import handle_error_response
from cancergeonomics.http.exceptions import AuthTokenException

if sys.version_info[0] >= 3:
    from urllib.parse import urljoin
else:
    from urlparse import urljoin

logger = logging.getLogger(__name__)

CLIENT_INFO = {
    'version': cancergeonomics.__version__,
    'os': platform.system(),
    'python': platform.python_version(),
    'requests': requests.__version__,
}


class BaseSession(requests.Session):
    pass


class CGCBaseHttpClient(object):
    """
    Base Http Client Class for handling API requests
    """

    def __init__(self, token, api='https://cgc-api.sbgenomics.com/v2/', timeout=30):
        """
        :param token: Authorization token which will be used in X-SBG-Auth-Token header
        :param api: Root API Url
        :param timeout: Request timeout value
        """
        self.api = api
        self.token = token

        if not self.token:
            raise AuthTokenException("Authentication token must be provided")

        # Initialization of Session
        self.session = BaseSession()
        self.timeout = timeout

        # Setting up default headers
        self.headers = {
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent':
                'cancergeonoomics-python-client/{version} ({os}, Python/{python}; '
                'requests/{requests})'.format(**CLIENT_INFO),
            "X-SBG-Auth-Token": token
        }

    def _request(self, method, url, headers=None, params=None, data=None, append_url=True):
        """
        :param method: Used for defining HTTP Request method GET, POST, PUT, PATCH, HEAD, OPTIONS
        :param url: Used as url or absolute url if append_url=False on which request will be send
        :param headers: Request headers which can be additionally added,
         but it won't override default headers
        :param params: Query params which will be send with request
        :param data: Body data which will be sent
        :param append_url: Bollean value
        :return: Http Response content data as Dict
        """
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
        """
        This method performs GET Http Request
        :return: HTTP Response
        """
        return self._request('GET', url, headers, query_params, data, append_url)

    def post(self, url, headers=None, query_params=None, data=None, append_url=True):
        """
        This method performs POST Http Request
        :return: HTTP Response
        """
        return self._request('POST', url, headers, query_params, data, append_url)

    def put(self, url, headers=None, query_params=None, data=None, append_url=True):
        """
        This method performs PUT Http Request
        :return: HTTP Response
        """
        return self._request('PUT', url, headers, query_params, data, append_url)

    def patch(self, url, headers=None, query_params=None, data=None, append_url=True):
        """
        This method performs PATCH Http Request
        :return: HTTP Response
        """
        return self._request('PATCH', url, headers, query_params, data, append_url)

    def delete(self, url, headers=None, query_params=None, data=None, append_url=True):
        """
        This method performs DELETE Http Request
        :return: HTTP Response
        """
        return self._request('DELETE', url, headers, query_params, data, append_url)

    @staticmethod
    def download(url, file_path, stream=True, chunk_size=8192, query_params=None):
        logger.info("Download started to %s", file_path)
        download_obj = Download(url, file_path, stream, chunk_size, query_params=query_params)
        return download_obj.download()
