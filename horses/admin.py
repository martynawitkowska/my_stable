from django.contrib import admin

from . import models


@admin.register(models.Horse)
class HorseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'mother', 'father', 'birth_date')}

