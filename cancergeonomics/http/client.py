import json
import platform
from urllib.parse import urljoin

import pkg_resources
import requests

from cancergeonomics.http.download import Download
from cancergeonomics.http.error_handlers import handle_error_response

client_info = {
    'version': pkg_resources.get_distribution('cancergeonomics').version,
    'os': platform.system(),
    'python': platform.python_version(),
    'requests': requests.__version__,
}

from cancergeonomics.http.exceptions import AuthTokenException


class BaseSession(requests.Session):
    pass


class CGCBaseHttpClient(object):
    def __init__(self, token, api='https://cgc-api.sbgenomics.com/v2/', timeout=60):
        self.api = api
        self.token = token
        self.session = BaseSession()
        self.timeout = timeout
        self.headers = {
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent':
                'sevenbridges-python/{version} ({os}, Python/{python}; '
                'requests/{requests})'.format(**client_info)
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

        resp = self.session.request(method, url, headers=headers, params=params, data=json.dumps(data))

        if not resp.ok:
            handle_error_response(resp)

        return self.process_response(resp)

    def process_response(self, resp):
        data = resp.json()
        if 'items' in data:
            return data['items']
        return data

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

    def download(self, url, file_path, stream=True, chunk_size=8192):
        d = Download(url, file_path, stream, chunk_size)
        return d.run_download()


