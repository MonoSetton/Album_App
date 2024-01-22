from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUsername(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']


class UpdateEmail(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

