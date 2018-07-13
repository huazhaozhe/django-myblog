#!/usr/bin/env python
# coding=utf-8

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'icon_prefix2', 'class': 'simditor', 'length': '5000'}))

    class Meta:
        model = Comment
        fields = ['text']
