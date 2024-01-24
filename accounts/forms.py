from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



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


class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'your old Password',  'class' : 'span'}))
    newpassword1 = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New Password',  'class' : 'span'}))
    newpassword2 = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password',  'class' : 'span'}))

    def clean(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data


