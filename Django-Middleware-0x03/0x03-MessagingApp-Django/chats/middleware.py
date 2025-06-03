from datetime import datetime, time
from django.http import HttpResponseForbidden
import logging

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
