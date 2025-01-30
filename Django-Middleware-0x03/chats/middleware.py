from django.utils import timezone


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine the user
        user = request.user.email if request.user.is_authenticated else 'AnonymousUser'
        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"{timestamp} - User: {user} - Path: {request.path}\n"

        # Write to the log file
        with open('requests.log', 'a') as log_file:
            log_file.write(log_message)

        response = self.get_response(request)
        return response
