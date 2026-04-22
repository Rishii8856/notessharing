import time
from .models import VisitorLog

class VisitorMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()
        duration = int(end_time - start_time)

        ip = request.META.get('REMOTE_ADDR')

        VisitorLog.objects.create(
            ip_address=ip,
            duration=duration
        )

        return response