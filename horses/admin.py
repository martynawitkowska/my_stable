from django.contrib import admin

from . import models

admin.site.register(models.Feeding)
admin.site.register(models.Training)


class TrainingInline(admin.StackedInline):
    model = models.Training


@admin.register(models.Horse)
class HorseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'mother', 'father', 'birth_date')}
    inlines = (TrainingInline, )
