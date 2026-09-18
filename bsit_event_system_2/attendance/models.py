from django.db import models
from accounts.models import Profile
from events.models import Event

class Attendance(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="attendance_records")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendance_records")
    in_at = models.DateTimeField(null=True, blank=True)
    out_at = models.DateTimeField(null=True, blank=True)
    in_scanned_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="attendance_in_scans"
    )
    out_scanned_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="attendance_out_scans"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "event"],
                name="unique_student_event_attendance",
            )
        ]
        ordering = ["-created_at"]

    @property
    def completed(self):
        return self.in_at is not None and self.out_at is not None

    @property
    def status(self):
        if self.completed:
            return "COMPLETED"
        if self.in_at:
            return "IN"
        return "PENDING"

    def __str__(self):
        return f"{self.student.display_name} - {self.event.name}"
