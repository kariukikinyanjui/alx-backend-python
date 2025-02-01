from django.utils import timezone
from datetime import datetime
from threading import Lock
from django.http import HttpResponseForbidden


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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour # Server's local time

        # Check if accessing chat endpoints during restricted hours
        if request.path.startswith('/api/conversations/') and (current_hour >= 21 or current_hour < 6):
            return HttpResponseForbidden("Chat access is restricted between 9 PM and 6 AM.")
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}
        self.lock = Lock()
        self.LIMIT = 5 # requests
        self.WINDOW = 60 # seconds

    def __call__(self, request):
        # Only check POST requests to messages endpoint
        if request.method == 'POST' and 'conversations' in request.path and 'messages' in requests.path:
            # Get client IP (handles proxies)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', '')

            current_time = time.time()

            with self.lock:
                # Cleanup old entries for this IP
                if ip in self.request_counts:
                    self.request_counts[ip] = [
                        t for t in self.request_counts[ip]
                        if current_time -t < self.WINDOW
                    ]

                    # Check rate limit
                    if len(self.request_counts[ip]) >= self.LIMIT:
                        return HttpResponseForbidden(
                            "Rate limit exceeded: 5 messages per minute allowed."
                        )

                    self.request_counts[ip].append(current_time)
                else:
                    self.request_counts[ip] = [current_time]

        return self.get_response(request)
