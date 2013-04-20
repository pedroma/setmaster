from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _


class SMSignupForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(), label=_("Email"))
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_("Repeat Password"))

    def clean_email(self):
        """ Validate that the e-mail address is unique. """
        if get_user_model().objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_('You are already registered. Please login instead.'))
        return self.cleaned_data['email']

    def clean(self):
        """
        Set the username to be hash of the email address.

        Generate a random password.

        Once activation occurs, we reset the password
        """

        # password = sha_constructor(str(random.random())).hexdigest()[:8]

        self.cleaned_data['username'] = self.cleaned_data.get('email', None)
        return self.cleaned_data
