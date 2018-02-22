from django.db import models

# Create your models here.

from django.conf import settings
from django.utils import timezone

oauth_type = (
        (1, 'github'),
        (2, 'weibo'),
        (3, 'qq'),
        )

class OauthUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    openid = models.CharField(max_length=100)
    nickname = models.CharField('昵称', max_length=100, blank=True)
    picture = models.CharField('头像', max_length=300, blank=True)
    token = models.CharField(max_length=150, blank=True)
    type = models.IntegerField('oauth类型', choices=oauth_type)
    email = models.EmailField('邮箱', blank=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        if self.nickname:
            return self.nickname
        elif self.email:
            return self.email
        else:
            return self.openid

    class Meta:
        verbose_name = 'oauth user'
