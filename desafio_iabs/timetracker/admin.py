from django.contrib import admin
from .models import Task, TimeEntry

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'created_at')
    search_fields = ('user__username', 'description')
    list_filter = ('created_at',)

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('task', 'entry_date', 'duration', 'description', 'created_at')
    search_fields = ('task__description', 'description')
    list_filter = ('entry_date', 'created_at')