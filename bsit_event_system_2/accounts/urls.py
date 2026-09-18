from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("student-login/", views.student_login, name="student_login"),
    path("organizer-login/", views.organizer_login, name="organizer_login"),
    path("register/", views.register_student, name="register_student"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("profile/", views.profile, name="profile"),
]