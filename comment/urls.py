#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post/(?P<post_pk>[0-9]+)/(?P<parent_comment_pk>[0-9]+)/$',
        views.post_comment, name='post_comment'),
    url(r'^comment_delete/(?P<pk>[0-9]+)/$', views.comment_delete,
        name='comment_delete'),
    url(r'^comment_enable/(?P<pk>[0-9]+)/$', views.comment_enable,
        name='comment_enable'),
]
