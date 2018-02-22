"""djangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


handler404 = 'home.views.not_found'
handler500 = 'home.views.server_error'
handler403 = 'home.views.permission_denied'
handler400 = 'home.views.bad_request'

urlpatterns = [
    url(r'^master/', include(admin.site.urls)),
    url(r'^simditor/', include('simditor.urls')),
    #url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^account/', include('accounts.urls', namespace='account')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^oauth/', include('oauth.urls', namespace='oauth')),
    url(r'^comment/', include('comment.urls', namespace='comment')),
    url(r'^note/', include('note.urls', namespace='note')),
    url(r'', include('home.urls', namespace='home')),
]
