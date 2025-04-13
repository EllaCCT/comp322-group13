from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput,label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    email = forms.EmailField()
    address = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username','password1','password2','email','address')
        