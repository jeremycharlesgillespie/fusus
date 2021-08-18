from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password



class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        user = User.objects.get(email=email)
        if user is not None:
            if check_password(password, user.password):
                return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
