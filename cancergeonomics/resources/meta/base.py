import six


class ResourceMeta(type):

    def __new__(cls, name, bases, attrs):
        return type.__new__(cls, name, bases, attrs)

    def __get__(cls, instance, owner):
        cls.api_client = instance
        return cls


class Resource(six.with_metaclass(ResourceMeta)):
    RESOURCE_ROOT_URL = NotImplemented

    def __init__(self, api_client):
        self.api_client = api_client

    @classmethod
    def get(self, id, **query_params):
        """
        Send Http GET Request and return the list of items. Enables filtering by query params
        :param kwargs: Request query params
        :return: List of return Resource items
        """
        return self.api_client.get(self.detail_url(id), query_params=query_params)

    @classmethod
    def filter(self, **query_params):
        """
        Send Http GET Request on Resource url and return the list of items. Enables filtering by query params
        :param kwargs: Request query params
        :return: List of return Resource items
        """
        return self.api_client.get(self.RESOURCE_ROOT_URL, query_params=query_params)['items']

    @classmethod
    def update(self, id, data, **query_params):
        return self.api_client.patch(self.detail_url(id), data=data, query_params=query_params)

    @classmethod
    def detail_url(self, id):
        return self.RESOURCE_ROOT_URL.rstrip('/') + "/{}".format(id)
