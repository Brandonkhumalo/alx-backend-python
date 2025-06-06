from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden
import logging
from django.http import JsonResponse
from collections import defaultdict

# Set up logging configuration
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('request_logs.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_restrict = time(21, 0)  # 9 PM
        end_restrict = time(6, 0)     # 6 AM

        if now >= start_restrict or now < end_restrict:
            return HttpResponseForbidden("Access to the messaging app is restricted during these hours (9PM to 6AM).")

        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Track messages by IP: {ip: [datetime, datetime, ...]}
        self.message_log = defaultdict(list)
        self.time_window = timedelta(minutes=1)
        self.message_limit = 5

    def __call__(self, request):
        # Only limit POST requests to the message endpoint
        if request.method == "POST" and request.path.startswith("/messages"):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove timestamps outside the time window
            self.message_log[ip] = [
                timestamp for timestamp in self.message_log[ip]
                if now - timestamp < self.time_window
            ]

            if len(self.message_log[ip]) >= self.message_limit:
                return JsonResponse(
                    {"detail": "Message rate limit exceeded. Max 5 messages per minute."},
                    status=429
                )

            # Log current timestamp
            self.message_log[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Handle X-Forwarded-For for reverse proxies
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce role checks on authenticated users
        user = request.user
        if user.is_authenticated:
            # Customize your paths if needed
            protected_paths = ['/admin-only/', '/moderator-only/']

            if any(request.path.startswith(path) for path in protected_paths):
                if user.role not in ['admin', 'moderator']:
                    return JsonResponse(
                        {"detail": "Access denied: insufficient permissions."},
                        status=403
                    )

        return self.get_response(request)