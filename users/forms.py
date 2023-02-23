from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField, UserChangeForm, \
    PasswordResetForm

from base.forms import StyleFormMixin
from users.models import User


class SigninForm(StyleFormMixin, AuthenticationForm):
    pass


class SignupForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)
        field_classes = {'username': UsernameField}


class CustomEditUserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country')


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    pass
