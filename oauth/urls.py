#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^github_login/$', views.github_login, name='github_login'),
    url(r'^github_check/$', views.github_check, name='github_check'),
    # url(r'^bind_email/$', views.bind_email, name='bind_email'),
]
