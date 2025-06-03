import logging
from datetime import datetime

# Set up a logger
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("user_requests.log")  # File where logs will be stored
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Required initialization step

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)  # Proceed to the next middleware/view
        return response