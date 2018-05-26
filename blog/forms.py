#!/usr/bin/env python
# coding=utf-8

from django import forms
from django.forms import widgets
from accounts.models import User
from .models import Post
# from ckeditor.widgets import CKEditorWidget

from django.utils.encoding import force_text
from django.forms.utils import flatatt
from django.utils.html import format_html


class MyCheckboxInput(forms.CheckboxInput):

    def __init__(self, span='span'):
        forms.CheckboxInput.__init__(self)
        self.span = span

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
        if not (value is True or value is False or value is None or value == ''):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)

        html = format_html('<p><label><input{} /><span>' + self.span + '</span></label></p>', flatatt(final_attrs))
        return html


class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=True), empty_label=None)
    excerpt = forms.CharField(required=False)
    body = forms.CharField(widget=widgets.Textarea(attrs={'class': 'ckeditor'}))
    json_data = forms.CharField(widget=widgets.TextInput(attrs={
        'id': 'json_data',
        'style': 'display:none;'
    }), required=False)
    visible = forms.BooleanField(widget=MyCheckboxInput(span='可见'), required=False)
    comment_enabled = forms.BooleanField(widget=MyCheckboxInput(span='评论'), required=False)

    class Meta:
        model = Post
        exclude = ['created_time', 'views', 'modified_time']
