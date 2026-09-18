from django import forms
from django.contrib.auth.models import User

from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            "name",
            "description",
            "date",
            "start_time",
            "end_time",
            "venue",
            "organizer",
            "image",
            "stamp_design",
            "status",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "start_time": forms.TimeInput(
                attrs={"type": "time"}
            ),

            "end_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        # Only show organizer choices to Admin/staff
        if user and not user.is_staff:

            if "organizer" in self.fields:
                self.fields.pop("organizer")

        else:

            self.fields["organizer"].queryset = User.objects.filter(
                profile__role="ORGANIZER"
            )