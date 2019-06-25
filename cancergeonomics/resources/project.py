from cancergeonomics.resources.base import Resource


class ProjectResource(Resource):

    def list(self, query_params=None):
        res = self.api_client.get('projects', query_params=query_params)
        return res

