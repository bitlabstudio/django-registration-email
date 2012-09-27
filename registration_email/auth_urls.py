"""
Re-definition of Django's auth URLs.

This is done for convenience. It allows us to save all registration and auth
related templates in the same `/templates/registration/` folder.

"""
from django.conf.urls.defaults import url, patterns
from django.contrib.auth import views as auth_views
from registration_email.forms import EmailAuthenticationForm


urlpatterns = patterns('',
    url(r'^login/$',
        auth_views.login,
        {'template_name': 'registration/login.html',
         'authentication_form': EmailAuthenticationForm,
        },
        name='auth_login',
    ),
    url(r'^logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.html'},
        name='auth_logout',
    ),
    url(r'^password/change/$',
        auth_views.password_change,
        {'template_name': 'registration/password_change_form_custom.html'},
        name='auth_password_change',
    ),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'registration/password_change_done_custom.html'},
        name='auth_password_change_done',
    ),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'template_name': 'registration/password_reset_form.html'},
        name='auth_password_reset',
    ),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html'},
        name='auth_password_reset_confirm',
    ),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'registration/password_reset_complete.html'},  # NOQA
        name='auth_password_reset_complete',
    ),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'registration/password_reset_done.html'},
        name='auth_password_reset_done',
    ),
)
