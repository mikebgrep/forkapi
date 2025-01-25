from django.contrib import admin

from .models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'date', 'timing']

    pass


admin.site.register(Schedule, ScheduleAdmin)