#!/usr/bin/env python
# coding=utf-8

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import User

class LoginForm(AuthenticationForm):
    next = forms.CharField(max_length=100, required=False)

    class Meta:
        fields = ['username', 'password', 'next']


class RegisterForm(UserCreationForm):
    next = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'next']
