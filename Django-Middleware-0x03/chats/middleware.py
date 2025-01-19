import logging
from datetime import datetime
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s',
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current server time
        current_hour = datetime.now().hour

        # Define restricted hours (outise 9AM - 6AM)
        if current_hour < 9 or current_hour > 18:
            return HttpResponseForbidden("Access to the chat is restricted outside of 9AM to 6PM.")

        # Proceed with the request if within allowed hours
        return self.get_response(request)
