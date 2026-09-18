from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "event", "in_at", "out_at", "in_scanned_by", "out_scanned_by")
    list_filter = ("event",)
    search_fields = ("student__student_id", "student__user__first_name", "student__user__last_name", "event__name")
