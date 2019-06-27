from cancergeonomics.resources.meta.base import Resource


class ProjectResource(Resource):
    RESOURCE_ROOT_URL = 'projects'

    @classmethod
    def list(cls, **query_params):
        """
        :param kwargs: query params
        :return: list of Project items
        """
        return cls.filter(**query_params)
