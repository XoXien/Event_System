from django.contrib import admin
from .models import EventStamp

@admin.register(EventStamp)
class EventStampAdmin(admin.ModelAdmin):
    list_display = ("student", "event", "earned_at")
    list_filter = ("event", "earned_at")
    search_fields = ("student__student_id", "student__user__first_name", "student__user__last_name", "event__name")
