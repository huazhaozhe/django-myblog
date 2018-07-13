#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.NoteIndexView.as_view(), name='index'),
    # url(r'^note_edit/(?P<pk>[0-9]+)/$', views.add_or_edit, name='note_edit'),
    url(r'^note_edit/(?P<pk>[0-9]+)?$', views.NoteAddOrEditView.as_view(),
        name='note_edit'),
    url(r'^like/(?P<note_pk>[0-9]+)/$', views.note_like, name='like'),
    url(r'^note_delete/(?P<note_pk>[0-9]+)/$', views.note_delete,
        name='note_delete'),
    url(r'^note_visible/(?P<note_pk>[0-9]+)/$', views.note_visible,
        name='note_visible'),
]
