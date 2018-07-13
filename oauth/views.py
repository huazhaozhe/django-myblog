from django.shortcuts import render, redirect, render_to_response

# Create your views here.

from .oauth_client import GithubOauth, WeiboOauth
from accounts.models import User
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import Permission
from django.core.mail import send_mail
from .models import OauthUser
import time

from_email = settings.EMAIL_HOST_USER
to_email = [settings.ADMINS[0][1]]


def github_login(request):
    github_oauth = GithubOauth(settings.OAUTH['github']['client_id'],
                               settings.OAUTH['github']['client_secret'],
                               settings.OAUTH['github']['redirect_url'])
    url = github_oauth.get_auth_url()
    next = request.GET.get('next', '/')
    response = redirect(url)
    response.set_cookie('next', next)
    return response


def github_check(request):
    next = request.COOKIES.get('next', '/')
    type = 1
    request_code = request.GET.get('code')
    github_oauth = GithubOauth(settings.OAUTH['github']['client_id'],
                               settings.OAUTH['github']['client_secret'],
                               settings.OAUTH['github']['redirect_url'])
    try:
        access_token = github_oauth.get_access_token(request_code)
        time.sleep(0.1)
        infos = github_oauth.get_user_info()
        openid = infos.get('id', '')
        oauth_user = OauthUser.objects.filter(openid=openid, type=type)
        if oauth_user:
            if oauth_user[0].user.enable:
                oauth_user[
                    0].user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, oauth_user[0].user)
                response = redirect(next)
                response.delete_cookie('next')
                return response
            else:
                return redirect('account:login')
        nickname = infos.get('name', 'github' + str(openid)[::2])
        picture = infos.get('avatar_url', '')
        token = access_token
        email = github_oauth.get_email()
        user = User(username='github' + str(openid), nickname=nickname,
                    email=email, avatar_url=picture)
        user.save()
        user.user_permissions.add(
            Permission.objects.get(codename='add_comment'))
        user.user_permissions.add(Permission.objects.get(codename='add_note'))
        user = User.objects.get(pk=user.pk)
        oauth_user = OauthUser(user=user, openid=openid, nickname=nickname,
                               email=email, picture=picture, token=token,
                               type=type)
        oauth_user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        new_user_email_message = nickname + email
        try:
            send_mail('django-github新用户', new_user_email_message, from_email,
                      to_email)
        except:
            pass
        response = redirect(next)
        response.delete_cookie('next')
        return response
    except:
        try:
            send_mail('django-github登录错误', 'Error', from_email, to_email)
        except:
            pass
        return render(request, 'oauth/oauth_faild.html')


def weibo_login(request):
    weibo_oauth = WeiboOauth(settings.OAUTH['weibo']['client_id'],
                             settings.OAUTH['weibo']['client_secret'],
                             settings.OAUTH['weibo']['redirect_url'])
    url = weibo_oauth.get_auth_url()
    return redirect(url)


def weibo_check(request):
    type = 2
    request_code = request.GET.get('code')
    weibo_oauth = WeiboOauth(settings.OAUTH['weibo']['client_id'],
                             settings.OAUTH['weibo']['client_secret'],
                             settings.OAUTH['weibo']['redirect_url'])
    access_token = weibo_oauth.get_access_token(request_code)
    time.sleep(0.1)
    infos = weibo_oauth.get_user_info()
    openid = infos.get('id', '')
    oauth_user = OauthUser.objects.filter(openid=openid, type=type)
    if oauth_user:
        if oauth_user[0].user:
            if oauth_user[0].user.enable:
                oauth_user[
                    0].user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, oauth_user[0].user)
                return redirect('/')
    nickname = infos.get('name', 'weibo' + str(openid)[::2])
    picture = infos.get('avatar_url', '')
    token = access_token
    email = weibo_oauth.get_email()
    user = User(username='weibo' + str(openid), nickname=nickname, email=email,
                avatar_url=picture)
    user.save()
    user.user_permissions.add(Permission.objects.get(codename='add_comment'))
    user.user_permissions.add(Permission.objects.get(codename='add_note'))
    user = User.objects.get(pk=user.pk)
    oauth_user = OauthUser(user=user, openid=openid, nickname=nickname,
                           email=email, picture=picture, token=token, type=type)
    oauth_user.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('/')
