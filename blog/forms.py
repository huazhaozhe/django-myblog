#!/usr/bin/env python
# coding=utf-8

from django import forms
from django.forms import widgets
from accounts.models import User
from .models import Post
#from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):

    author = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=True), empty_label=None)
    excerpt = forms.CharField(required=False)
    body = forms.CharField(widget=widgets.Textarea(attrs={'class': 'ckeditor'}))
    json_data = forms.CharField(widget=widgets.TextInput(attrs={
        'id': 'json_data',
        'style': 'display:none;'
        }), required=False)

    class Meta:
        model = Post
        exclude = ['created_time', 'views', 'modified_time']

