from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import hashlib, urllib

class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=50, blank=True)
    avatar_url = models.CharField('头像', max_length=300, blank=True)
    created_time = models.DateTimeField('注册时间', default=timezone.now)
    enable = models.BooleanField(default=True)

    def __str__(self):
        if self.nickname:
            return self.nickname
        elif self.username:
            return self.username
        else:
            return self.pk
