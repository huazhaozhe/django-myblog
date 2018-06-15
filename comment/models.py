from django.db import models

# Create your models here.

from django.conf import settings
from blog.models import Post
#from note.models import Note
from accounts.models import User
from django.utils import timezone
from simditor.fields import RichTextField


class Comment(models.Model):
    text = RichTextField('评论')
    created_time = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    parent_comment = models.ForeignKey('self', verbose_name='上级评论', blank=True, null=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:20]
