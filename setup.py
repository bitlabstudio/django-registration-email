import os

from setuptools import setup, find_packages

import registration_email


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-registration-email",
    version=registration_email.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.md'),
    keywords='django, registration, email, backend',
    packages=find_packages(),
    author='Martin Brochhaus',
    author_email='martin.brochhaus@gmail.com',
    url="http://github.com/bitmazk/djangno-registration-email",
    include_package_data=True,
    test_suite='registration_email.tests.runtests.runtests',
)
