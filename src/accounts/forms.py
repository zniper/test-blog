from __future__ import unicode_literals

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Field

User = get_user_model()


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields["username"].widget.input_type = "email"  # ugly hack

        self.helper.layout = Layout(
            Field('username', placeholder="Enter Username", autofocus=""),
            Field('password', placeholder="Enter Password"),
            Field('remember_me'),
            Submit('sign_in', 'Log in',
                   css_class="btn btn-lg btn-primary btn-block"),
            )


class SignupForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'duplicate_username': _(
            "A user with that %(username)s already exists."),
    }

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above,"
                                            " for verification."))

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD,) + tuple(User.REQUIRED_FIELDS)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        def validate_uniqueness_of_username_field(value):
            # Since User.username is unique, this check is redundant,
            # but it sets a nicer error message than the ORM. See #13147.
            try:
                User._default_manager.get_by_natural_key(value)
            except User.DoesNotExist:
                return value
            raise forms.ValidationError(
                self.error_messages['duplicate_username'] % {
                    'username': User.USERNAME_FIELD,
                    }
                )

        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields[User.USERNAME_FIELD].validators.append(
            validate_uniqueness_of_username_field)
        del self.fields["email"]

        self.helper.layout = Layout(
            Field('username', placeholder="Enter Username"),
            Field('password1', placeholder="Enter Password"),
            Field('password2', placeholder="Re-enter Password"),
            Submit('sign_up', 'Sign up', css_class="btn-warning"),
            )
