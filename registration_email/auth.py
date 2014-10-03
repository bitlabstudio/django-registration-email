"""
Custom authentication backends.

Inspired by http://djangosnippets.org/snippets/2463/

"""
from django.contrib.auth.backends import ModelBackend
from django.core.validators import validate_email


try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows to login with an email address.

    """

    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        try:
            validate_email(username)
        except:
            username_is_email = False
        else:
            username_is_email = True
        if username_is_email:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            # We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
