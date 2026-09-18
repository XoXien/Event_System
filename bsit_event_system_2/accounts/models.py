from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        ORGANIZER = "ORGANIZER", "Event Organizer"
        STUDENT = "STUDENT", "Student"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    student_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    program = models.CharField(max_length=100, blank=True)
    year_level = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.role}"

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username
