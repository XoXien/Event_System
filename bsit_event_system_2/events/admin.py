from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "start_time", "venue", "organizer", "status")
    list_filter = ("status", "date")
    search_fields = ("name", "venue", "description")
