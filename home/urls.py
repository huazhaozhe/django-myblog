#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^error/$', views.error, name='error'),
]
