from django.contrib import admin

# Register your models here.

from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'visible']


admin.site.register(Note, NoteAdmin)
