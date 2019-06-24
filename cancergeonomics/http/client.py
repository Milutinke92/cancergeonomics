import json
import typing
from urllib.parse import urljoin

import pkg_resources
import requests
import platform
import cancergeonomics
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

    def _request(self, method, relative_url, headers=None, params=None, data=None):
        if headers:
            headers.update(self.session.headers)
        else:
            headers = self.headers

        url = urljoin(self.api, relative_url)
        resp = self.session.request(method, url, headers=headers, params=params, data=json.dumps(data))

        if not resp.ok:
            handle_error_response(resp)

        return self.process_response(resp)

    def process_response(self, resp):
        data = resp.json()
        if 'items' in data:
            return data['items']
        return data

    def get(self, url, headers=None, query_params=None, data=None):
        return self._request('GET', url, headers, query_params)

    def post(self, url, headers=None, query_params=None, data=None):
        return self._request('POST', url, headers, query_params, data)

    def put(self, url, headers=None, query_params=None, data=None):
        return self._request('PUT', url, headers, query_params, data=data)

    def patch(self, url, headers=None, query_params=None, data=None):
        return self._request('PATCH', url, headers, query_params, data)

    def delete(self, url, headers=None, query_params=None, data=None):
        return self._request('DELETE', url, headers, query_params, data)
