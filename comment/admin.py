from django.contrib import admin

# Register your models here.

from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_time', 'text']

admin.site.register(Comment, CommentAdmin)
