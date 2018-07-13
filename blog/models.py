from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

from django.utils import timezone
from django.conf import settings
from simditor.fields import RichTextField
# from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField('分类', max_length=60, unique=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签', max_length=30, unique=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = (
        (0, '草稿'),
        (1, '发布'),
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField('标题', max_length=100)
    excerpt = models.CharField('摘要', max_length=1000, blank=True)
    # body = models.TextField('正文')
    body = RichTextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('最后修改时间', default=timezone.now)
    views = models.PositiveIntegerField('浏览量', default=0)
    comment_enabled = models.BooleanField('允许评论', default=True)
    visible = models.BooleanField('可见', default=True)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=0)
    category = models.ForeignKey(Category, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    json_data = models.CharField(max_length=1000, blank=True)

    class Meta:
        ordering = ('-created_time',)

    def get_comments(self):
        comment_parent_list = self.comment_set.filter(
            parent_comment=None).order_by('created_time')
        comment_child_list = self.comment_set.exclude(
            parent_comment=None).order_by('created_time')
        comment_list = []
        for comment in comment_parent_list:
            comment_list.append([comment, []])
        for comment in comment_child_list:
            for k, v in comment_list:
                if k.pk == comment.parent_comment.pk:
                    v.append(comment)
                    break
                else:
                    if v:
                        for i in v:
                            if i.pk == comment.parent_comment.pk:
                                v.append(comment)
                                break
        comment_list.reverse()
        return comment_list

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title
