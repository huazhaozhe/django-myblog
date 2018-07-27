# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author   : zhe
# @File     : middleware.py
# @Time     : 2018/07/26 19:40
# @Software : PyCharm


from django.core.cache import cache
from django.conf import settings
from robotkiller.models import AddrKiller
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden

forbidden_str = '''
<br>
<div align="center">
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
    <path d="M0 0h24v24H0z" fill="none"/>
    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8 0-1.85.63-3.55 1.69-4.9L16.9 18.31C15.55 19.37 13.85 20 12 20zm6.31-3.1L7.1 5.69C8.45 4.63 10.15 4 12 4c4.42 0 8 3.58 8 8 0 1.85-.63 3.55-1.69 4.9z"/>
</svg>
</div>
<h1 align="center">addr %s access forbidden</h1>
'''


class BlockedIpMiddleware():

    def process_request(self, request):
        if cache.get('ban_init') != 1 or not hasattr(self, 'ban_init'):
            self.get_ban_addr()
        addr = request.META['REMOTE_ADDR']
        if not request.user.is_superuser and addr not in settings.BAN_WHITE \
                and settings.BAN_STATUS:
            if cache.ttl(addr) == 0:
                cache.set(addr, 1, timeout=settings.BAN_CYCLE)
            elif cache.ttl(addr) is None:
                return HttpResponseForbidden(forbidden_str % addr)
            elif cache.ttl(addr) > 0:
                num = cache.get(addr)
                if num + 1 > settings.BAN_COUNT:
                    self.check_addr(addr)
                    return HttpResponseForbidden(forbidden_str % addr)
                elif num == -1:
                    return HttpResponseForbidden(forbidden_str % addr)
                else:
                    cache.set(addr, num + 1, timeout=cache.ttl(addr))

    def check_addr(self, addr):
        ban_addr = AddrKiller.objects.get_or_create(addr=addr)
        ban_num = ban_addr[0].count
        if ban_num + 1 > settings.BAN_MAX:
            ban_addr[0].status = True
            ban_addr[0].status_time = datetime.now()
            cache.set(addr, -1, timeout=None)
        else:
            ban_addr[0].unlock_time = datetime.now() + timedelta(
                seconds=settings.BAN_TIME)
            cache.set(addr, -1, timeout=settings.BAN_TIME)
        ban_addr[0].count = ban_num + 1
        ban_addr[0].save()

    def get_ban_addr(self):
        addrs = AddrKiller.objects.all()
        for addr in addrs:
            if addr.status:
                cache.set(addr.addr, -1, timeout=None)
            elif addr.unlock_time > datetime.now():
                unlock_timeout = addr.unlock_time - datetime.now()
                cache.set(addr.addr, -1, timeout=unlock_timeout.total_seconds())
        cache.set('ban_init', 1, timeout=None)
        self.ban_init = True
