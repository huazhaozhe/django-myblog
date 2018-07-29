from django.contrib import admin

# Register your models here.

from robotkiller.models import AddrKiller

class AddrKillerAdmin(admin.ModelAdmin):
    pass

admin.site.register(AddrKiller, AddrKillerAdmin)