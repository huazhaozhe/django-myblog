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


def get_ban_addr():
    print('get_ban_addr')
    addrs = AddrKiller.objects.all()
    for addr in addrs:
        if addr.status:
            cache.set(addr, settings.BAN_MAX, timeout=None)
        elif addr.unlock_time > datetime.now():
            unlock_timeout = addr.unlock_time - datetime.now()
            cache.set(addr, -1, timeout=unlock_timeout.total_seconds())


class BlockedIpMiddleware():

    def process_request(self, request):
        if not hasattr(self, 'ban_init'):
            get_ban_addr()
            self.ban_init = 1
        addr = request.META['REMOTE_ADDR']
        if cache.ttl(addr) == 0:
            cache.set(addr, 1, timeout=settings.BAN_CYCLE)
        elif cache.ttl(addr) > 0:
            num = cache.get(addr)
            if num + 1 >= settings.BAN_COUNT:
                self.check_addr(addr)
                raise PermissionDenied
            elif num == -1:
                raise PermissionDenied
            else:
                cache.set(addr, num + 1, timeout=cache.ttl(addr))
        elif cache.ttl(addr) is None:
            raise PermissionDenied

    def check_addr(self, addr):
        ban_addr = AddrKiller.objects.get_or_create(addr=addr)
        ban_num = ban_addr[0].count
        if ban_num + 1 >= settings.BAN_MAX:
            ban_addr[0].status = True
            ban_addr[0].status_time = datetime.now()
            cache.set(addr, settings.BAN_MAX, timeout=None)
        else:
            ban_addr[0].unlock_time = datetime.now() + timedelta(
                seconds=settings.BAN_TIME)
            cache.set(addr, -1, timeout=settings.BAN_TIME)
        ban_addr[0].count = ban_num + 1
        ban_addr[0].save()
