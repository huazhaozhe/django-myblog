from django.contrib import admin

# Register your models here.

from middleware.models import AddrKiller


class AddrKillerAdmin(admin.ModelAdmin):
    list_display = ['addr', 'status', 'status_time', 'count', 'unlock_time',
                    'user_agent']


admin.site.register(AddrKiller, AddrKillerAdmin)
