from django.contrib import admin

# Register your models here.

from middleware.models import AddrKiller


class AddrKillerAdmin(admin.ModelAdmin):
    pass


admin.site.register(AddrKiller, AddrKillerAdmin)
