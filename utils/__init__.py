from django.http import HttpResponse

class HttpResponseNotImplemented(HttpResponse):
    """
    HTTP 501 response: Not Implemented
    Use as a placeholder for stuff that'll work one day
    """
    status_code = 501