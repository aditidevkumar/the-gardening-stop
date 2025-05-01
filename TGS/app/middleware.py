# middleware.py
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

class AdminSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            request.session_key = f"admin_{request.session.session_key}"
        super().process_request(request)

class CustomerSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            request.session_key = f"customer_{request.session.session_key}"
        super().process_request(request)
        
