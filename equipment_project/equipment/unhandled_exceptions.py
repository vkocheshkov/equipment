from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.views import exception_handler


class UnhandledExceptionProcessorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if not isinstance(exception, Exception):
            return None

        if not isinstance(exception, APIException):
            status_code = status.HTTP_400_BAD_REQUEST

        return JsonResponse(
            {"error": True, "description": str(exception)}, status=status_code)
    

