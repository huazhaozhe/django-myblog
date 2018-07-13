from django.contrib import admin

# Register your models here.

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'nickname', 'email', 'created_time']


admin.site.register(User, UserAdmin)
