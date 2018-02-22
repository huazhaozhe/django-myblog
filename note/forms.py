#!/usr/bin/env python
# coding=utf-8

from django import forms
from .models import Note


class NoteForm(forms.ModelForm):

    VISIBLE_CHOICES = (
            (True, '公开'),
            (False, '仅自己可见'),
            )

    content = forms.CharField(label='详情', widget=forms.widgets.Textarea(attrs={'class': 'simditor'}), required=False)
    visible = forms.ChoiceField(label='是否公开', choices=VISIBLE_CHOICES)

    def clean(self):
        note = super(NoteForm, self).clean()
        title = note.get('title')
        content = note.get('content')
        image_url = note.get('image_url')
        if content and not image_url:
            raise forms.ValidationError('有详情必须需要图片链接')
        if not title and not image_url:
            raise forms.ValidationError('标题和图片链接不可同时为空')

    class Meta:
        model = Note
        fields = ['title', 'content', 'image_url', 'visible']

