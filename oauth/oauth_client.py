#!/usr/bin/env python
# coding=utf-8


import json
import urllib


class BaseOauth():
    def __init__(self, client_id, client_key, redirect_url):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def get(self, url, data):
        request_url = '%s?%s' % (url, urllib.parse.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    def post(self, url, data):
        request = urllib.request.Request(url, data=urllib.parse.urlencode(
            data).encode(encoding='UTF8'))
        response = urllib.request.urlopen(request)
        return response.read()

    def get_email(self):
        params = {
            'access_token': self.access_token,
        }
        response = self.get(self.API_EMAIL_URL, params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']


class GithubOauth(BaseOauth):
    AUTH_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    API_USER_URL = 'https://api.github.com/user'
    API_EMAIL_URL = 'https://api.github.com/user/emails'

    def get_auth_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_url': self.redirect_url,
            'scope': 'user',
            'state': 1
        }
        url = self.AUTH_URL + '?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self, code):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'code': code,
            'redirect_url': self.redirect_url,
        }
        response = self.post(self.ACCESS_TOKEN_URL, params)
        result = urllib.parse.parse_qs(response, True)
        self.access_token = result[b'access_token'][0]
        return self.access_token

    def get_user_info(self):
        params = {'access_token': self.access_token}
        response = self.get(self.API_USER_URL, params)
        result = json.loads(response.decode('utf-8'))
        return result


class WeiboOauth(BaseOauth):
    AUTH_URL = 'https://api.weibo.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    API_USER_URL = 'https://api.weibo.com/2/users/show.json'
    API_EMAIL_URL = 'https://api.weibo.com/2/account/profile/email.json'

    def get_auth_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_url,
            'scope': 'email',
            'state': 1
        }
        url = self.AUTH_URL + '?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_url
        }
        response = self.post(self.ACCESS_TOKEN_URL, params)
        result = json.loads(response.decode('utf-8'))
        self.access_token = result['access_token']
        self.openid = result['uid']
        return self.access_token

    def get_open_id(self):
        return self.openid

    def get_user_info(self):
        params = {
            'access_token': self.access_token,
            'uid': self.openid,
        }
        response = self.get(self.API_URL, params)
        result = json.loads(response.decode('utf-8'))
        return result
