"""Custom registration forms that expects an email address as a username."""
import md5

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}


def generate_username(email):
    return md5.new(email).hexdigest()[0:30]


class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(
            label=_("Email"), max_length=256)


class EmailRegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.

    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=256)),
        label=_("Email")
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
         label=_("Password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
         label=_("Password (repeat)"))

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        email = self.cleaned_data['email']
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            _('A user with that email already exists.'))

    def clean(self):
        """
        Verifiy that the values entered into the two password fields match.

        Note that an error here will end up in ``non_field_errors()`` because
        it doesn't apply to a single field.

        """
        data = self.cleaned_data
        if not 'email' in data:
            return data
        if ('password1' in data and 'password2' in data):

            if data['password1'] != data['password2']:
                raise forms.ValidationError(
                    _("The two password fields didn't match."))

        self.cleaned_data['username'] = generate_username(data['email'])
        return self.cleaned_data
