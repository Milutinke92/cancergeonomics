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
    def get(self, id, **kwargs):
        """
        Send Http GET Request and return the list of items. Enables filtering by query params
        :param kwargs: Request query params
        :return: List of return Resource items
        """
        return self.api_client.get(self.detail_url(id), query_params=kwargs)

    @classmethod
    def filter(self, **kwargs):
        """
        Send Http GET Request on Resource url and return the list of items. Enables filtering by query params
        :param kwargs: Request query params
        :return: List of return Resource items
        """
        return self.api_client.get(self.RESOURCE_ROOT_URL, query_params=kwargs)['items']

    @classmethod
    def update(self, id, data, **kwargs):
        return self.api_client.patch(self.detail_url(id), data=data, query_params=kwargs)

    @classmethod
    def detail_url(self, id):
        return self.RESOURCE_ROOT_URL.rstrip('/') + "/{}".format(id)
