from django.db import models
from accounts.models import Profile
from events.models import Event

class EventStamp(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="event_stamps")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="stamps")
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "event"],
                name="unique_student_event_stamp",
            )
        ]
        ordering = ["-earned_at"]

    def __str__(self):
        return f"{self.student.display_name} - {self.event.name}"
