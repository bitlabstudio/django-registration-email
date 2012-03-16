django-registration-email
==========================

We use
[django-registration](https://bitbucket.org/ubernostrum/django-registration/overview)
in almost all our projects. However, we don't like Django's limited username
and would like to allow our users to sign up via email.

This project provides a custom authentication backend which allows a user to
authenticate via his email. We also provide an EmailRegistrationForm which
checks if an email has already been taken.

Since we still have to store a username and since emails can easily be longer
than 30 characters, the username will be computed as a md5 hexdigest of the
email address.

We included a ``urls.py`` that overrides all URLs of django-registration
and Django's auth with a clean and sane structure and you will find a default
set of all necessary templates.
