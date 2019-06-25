class AuthTokenException(Exception):
    """
    Exception which will be raised if Authentication Token is not provided to HttpClient
    """


class BaseCGCHttpException(Exception):
    """
    The proper way is to add all exceptions that could happen on platform
    """


class FileDownloadException(Exception):
    """
    Exception which will be raised if provided url doesn't containt downloadable content
    """
