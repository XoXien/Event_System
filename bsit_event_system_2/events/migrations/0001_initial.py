from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("venue", models.CharField(max_length=200)),
                ("image", models.ImageField(blank=True, null=True, upload_to="events/")),
                ("stamp_design", models.ImageField(blank=True, null=True, upload_to="stamps/")),
                ("status", models.CharField(choices=[("UPCOMING", "Upcoming"), ("ONGOING", "Ongoing"), ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled")], default="UPCOMING", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("organizer", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="organized_events", to="auth.user")),
            ],
            options={"ordering": ["-date", "-start_time"]},
        ),
    ]
