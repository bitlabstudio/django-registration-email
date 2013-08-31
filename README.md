django-registration-email
==========================

We use
[django-registration](https://bitbucket.org/ubernostrum/django-registration/overview)
in almost all our projects. However, we don't like Django's limited username
and would like to allow our users to sign up via email.

This project provides a custom authentication backend which allows users to
authenticate via email. We also provide an EmailRegistrationForm which
checks if an email has already been taken.

Since we still have to store a username and since emails can easily be longer
than 30 characters, the username will be computed as a md5 hexdigest of the
email address.

We included a ``urls.py`` that overrides all URLs of django-registration
and Django's auth with a clean and sane structure and you will find a default
set of all necessary templates.

Usage
======

Install this package::

    pip install -e git://github.com/bitmazk/django-registration-email#egg=registration_email

Add ``registration`` and ``registration_email`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # all your other apps
        'registration',
        'registration_email',
    ]

Update your ``urls.py``::

    url(r'^accounts/', include('registration_email.backends.default.urls')),

Add some settings to your ``settings.py``::

    ACCOUNT_ACTIVATION_DAYS = 7
    AUTHENTICATION_BACKENDS = (
        'registration_email.auth.EmailBackend',
    )
    LOGIN_REDIRECT_URL = '/'

Run ``syncdb``::

    ./manage.py syncdb

Settings
========

django-registration-email introduces a new setting:

REGISTRATION_EMAIL_ACTIVATE_SUCCESS_URL
---------------------------------------

Default: ``lambda request, user: '/'``

Function to return the URL to redirect to after a successful account
activation. If you leave this at ``lambda request, user: '/'`` it will direct
to your base URL.

REGISTRATION_EMAIL_REGISTER_SUCCESS_URL
---------------------------------------

Default: ``lambda request, user: '/'``

Function to return the URL to redirect to after a successful account
registration. If you leave this at ``lambda request, user: '/'`` it will direct
to your base URL.

How to use a custom form
========================

Let's say you want to collect the user's first name and last name when he
registers. In order to achieve that, you need to do the following:

__1. Create a custom form__

Create a new app `my_registration` in your project and give it a `forms.py`
where you override our `EmailRegistrationForm` and your desired extra
fields:

    from django import forms
    from registration_email.forms import EmailRegistrationForm

    class CustomEmailRegistrationForm(EmailRegistrationForm):
        first_name = forms.CharField()
        last_name = forms.CharField()

Do NOT override the form's `save()` method.

__2. Override the URL__

Now you need to tell the registration view that it is supposed to use the
custom form:

    # your main urls.py
    ...
    from django.conf import settings
    from registration.views import register
    from my_registration.forms import CustomEmailRegistrationForm

    urlpatterns = patterns(
        '' ,
        ...
        url(r'^accounts/register/$',
            register,
            {'backend': 'registration.backends.simple.SimpleBackend',
            'template_name': 'registration/registration_form.html',
            'form_class': CustomEmailRegistrationForm,
            'success_url': getattr(
                settings, 'REGISTRATION_EMAIL_REGISTER_SUCCESS_URL', None),
            },
            name='registration_register',
        ),

        url(r'^accounts/', include('registration_email.backends.default.urls')),
        ...
    )

__3. Create a signal handler__

In the `urls.py` above I'm using the `SimpleBackend`. When you have a look
at that [backend](https://github.com/nathanborror/django-registration/blob/master/registration/backends/simple/__init__.py#L30)
you will see that the backend sends a signal after creating and logging in the
user. The signal will get all parameters that we need in order to access the
data that has been validated and sent by the form, so let's build a signal
handler:

    # in my_registration.models.py
    from django.dispatch import receiver
    from registration.signals import user_registered

    @receiver(user_registered)
    def user_registered_handler(sender, user, request, **kwargs):
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

This method has the drawback that you save the user two times in a row. If
you have concerns about performance you would have to create your own
`my_registration.backends.CustomRegistrationBackend` class. That class would
inherit `registration.backends.simple.SimpleBackend` and override the
`register` method.

But really, we are talking about registration here, I can't imagine how saving
the user twice could do any harm.


Troubleshooting
================

If you had another value for ``AUTHENTICATION_BACKENDS`` in your
``settings.py`` before it might be that it is saved in your ``django_session``
table. I found no other way around this than to delete the rows in that table.

TODO
=====

* Password reset link points to original django template
