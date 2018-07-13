from django.contrib import admin

# Register your models here.

from .models import OauthUser


class OauthUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'email', 'created_time']


admin.site.register(OauthUser, OauthUserAdmin)
