from django.contrib.auth.models import User
from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget = forms.TextInput, required = True)
    email = forms.CharField(widget=forms.TextInput, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UploadImage(forms.ModelForm):
    profilepic = forms.FileField()

    class Meta:
        model = Profile
        fields =['profilepic']


class UploadCover(forms.ModelForm):
    cover = forms.FileField(required=False)

    class Meta:
        model = WallPost
        fields = ['cover']