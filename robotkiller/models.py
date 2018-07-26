from django.db import models

# Create your models here.


from datetime import datetime, timedelta
from django.conf import settings

def default_unlock_time():
    return datetime.now() + timedelta(days=10)


class AddrKiller(models.Model):
    addr = models.CharField(max_length=100, unique=True)
    created_time = models.DateTimeField('首次记录日期', auto_now_add=True)
    unlock_time = models.DateTimeField('下次解封时间', default=default_unlock_time)
    count = models.IntegerField('封禁次数', default=0)
    status = models.BooleanField('永久封禁', default=False)
    status_time = models.DateTimeField('封禁时间', null=True)
