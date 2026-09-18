from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("accounts", "0001_initial"),
        ("events", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="EventStamp",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("earned_at", models.DateTimeField(auto_now_add=True)),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="stamps", to="events.event")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="event_stamps", to="accounts.profile")),
            ],
            options={"ordering": ["-earned_at"]},
        ),
        migrations.AddConstraint(
            model_name="eventstamp",
            constraint=models.UniqueConstraint(fields=("student", "event"), name="unique_student_event_stamp"),
        ),
    ]
