from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("student_id", "display_name", "role", "program", "year_level")
    list_filter = ("role", "program", "year_level")
    search_fields = ("student_id", "user__username", "user__first_name", "user__last_name")
