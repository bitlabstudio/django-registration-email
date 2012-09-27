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

Default: ``None``

The URL to redirect to after a successful account activation. If you leave this
at ``None`` the method ``post_activation_redirect`` of your registration
backend will be used.

REGISTRATION_EMAIL_REGISTER_SUCCESS_URL
---------------------------------------

Default: ``None``

The URL to redirect to after a successful registration. If you leave this at
``None`` the method ``post_registration_redirect`` of your registration backend
will be used.

Troubleshooting
================

If you had another value for ``AUTHENTICATION_BACKENDS`` in your
``settings.py`` before it might be that it is saved in your ``django_session``
table. I found no other way around this than to delete the rows in that table.

TODO
=====

* Password reset link points to original django template
