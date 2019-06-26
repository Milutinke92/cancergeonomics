from cancergeonomics.resources.meta.base import Resource


class ProjectResource(Resource):
    RESOURCE_ROOT_URL = 'projects'

    @classmethod
    def list(cls, **kwargs):
        return cls.filter(**kwargs)
