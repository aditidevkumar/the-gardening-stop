from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the user is a superuser (admin)
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                return super().authenticate(request, username, password, **kwargs)
            else:
                # If the user is not an admin, handle regular user authentication
                return User.objects.filter(username=username, is_superuser=False).first()
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

