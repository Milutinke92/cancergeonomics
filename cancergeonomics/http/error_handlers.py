from cancergeonomics.http.exceptions import BaseCGCHttpException


def handle_error_response(resp):
    """
    List of all HTTP Status Codes and Internal status codes:
    https://docs.cancergenomicscloud.org/docs/api-status-codes
    """
    exc_message = {
    }

    error_exc_klass = exc_message.get(resp.status_code, BaseCGCHttpException)

    error_exc = error_exc_klass(str(resp.json()))

    raise error_exc
