"""Custom urls.py for django-registration."""
from django.conf import settings
from django.conf.urls.defaults import include, url, patterns
from django.views.generic.simple import direct_to_template

from registration.views import activate, register
from registration_email.forms import EmailRegistrationForm


urlpatterns = patterns('',
    # django-registration views
    url(r'^activate/complete/$',
        direct_to_template,
        {'template': 'registration/activation_complete.html'},
        name='registration_activation_complete',
    ),
    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        {'backend': 'registration.backends.default.DefaultBackend',
         'template_name': 'registration/activate.html',
         'success_url': getattr(
             settings, 'REGISTRATION_EMAIL_ACTIVATE_SUCCESS_URL', None),
        },
        name='registration_activate',
    ),
    url(r'^register/$',
        register,
        {'backend': 'registration.backends.default.DefaultBackend',
         'template_name': 'registration/registration_form.html',
         'form_class': EmailRegistrationForm,
         'success_url': getattr(
             settings, 'REGISTRATION_EMAIL_REGISTER_SUCCESS_URL', None),
        },
        name='registration_register',
    ),
    url(r'^register/complete/$',
        direct_to_template,
        {'template': 'registration/registration_complete.html'},
        name='registration_complete',
    ),
    url(r'^register/closed/$',
        direct_to_template,
        {'template': 'registration/registration_closed.html'},
        name='registration_disallowed',
    ),

    # django auth urls
    url(r'', include('registration_email.auth_urls')),
)
