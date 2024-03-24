from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUsername(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username']


class UpdateEmail(UserChangeForm):
    email = forms.EmailField(required=True)
    password = None

    class Meta:
        model = User
        fields = ['email']


class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    oldpassword = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'Your old Password', 'class': 'span'}))
    newpassword1 = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'New Password', 'class': 'span'}))
    newpassword2 = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'type': 'password', 'placeholder': 'Confirm New Password', 'class': 'span'}))

    def clean(self):
        user = authenticate(username=self.request.user.username, password=self.cleaned_data['oldpassword'])
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise forms.ValidationError("The two password fields did not match.")
            if self.cleaned_data['newpassword1'] == self.cleaned_data['oldpassword']:
                raise forms.ValidationError("New password cannot be the same as old.")
            if user is None:
                raise forms.ValidationError("You have entered wrong old password.")

        return self.cleaned_data




