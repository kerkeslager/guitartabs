from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    email = forms.EmailField(help_text='This will be visible only to you')
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
        )

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

