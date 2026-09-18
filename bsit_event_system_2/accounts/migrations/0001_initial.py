from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("ADMIN", "Administrator"), ("ORGANIZER", "Event Organizer"), ("STUDENT", "Student")], default="STUDENT", max_length=20)),
                ("student_id", models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ("program", models.CharField(blank=True, max_length=100)),
                ("year_level", models.CharField(blank=True, max_length=50)),
                ("profile_image", models.ImageField(blank=True, null=True, upload_to="profiles/")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to="auth.user")),
            ],
        ),
    ]
