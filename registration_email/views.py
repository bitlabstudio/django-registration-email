"""Views for the registration_email app."""
from django.contrib.auth.views import login


def login_remember_me(request, *args, **kwargs):
    """Custom login view that enables "remember me" functionality."""
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return login(request, *args, **kwargs)
