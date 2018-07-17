#!/usr/bin/env python
# coding=utf-8

from django.conf.urls import url
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^$', cache_page(7 * 24 * 60 * 60)(views.home), name='home'),
    url(r'^about/$', cache_page(7 * 24 * 60 * 60)(views.about), name='about'),
]
