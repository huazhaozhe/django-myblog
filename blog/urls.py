#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url, include
from . import views

urlpatterns = [
        url(r'^$', views.PostIndexView.as_view(), name='index'),
        url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
        url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
        url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
        url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
        #url(r'^post_edit/(?P<pk>[0-9]+)/$', views.add_or_edit, name='post_edit'),
        url(r'^post_edit/(?P<pk>[0-9]+)?$', views.PostAddOrEditView.as_view(), name='post_edit'),
        url(r'^post_delete/(?P<pk>[0-9]+)/$', views.post_delete, name='post_delete'),
        url(r'^search/', include('haystack.urls')),
        ]
