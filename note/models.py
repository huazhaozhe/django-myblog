from django.db import models

# Create your models here.

from django.conf import settings


class Note(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField('标题', max_length=100, blank=True)
    content = models.CharField('详情', max_length=1000, blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    # image = models.ImageField('图片', blank=True)
    image_url = models.URLField('图片链接', blank=True)
    visible = models.BooleanField('所有人可见', default=True)
    likes = models.PositiveIntegerField('喜欢', default=0)

    class Meta:
        ordering = ('-created_time',)

    def increase_likes(self):
        self.likes += 1
        self.save(update_fields=['likes'])

    def __str__(self):
        if self.title:
            return self.title
        elif self.content:
            return self.content
        elif self.image_url:
            return self.image_url
        else:
            return self.pk
