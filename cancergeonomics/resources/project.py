from cancergeonomics.resources.base import Resource


class ProjectResource(Resource):
    RESOURCE_ROOT_URL = 'projects'

    def list(self, query_params=None):
        return self.filter(query_params=query_params)
