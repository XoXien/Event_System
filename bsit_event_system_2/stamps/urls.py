from django.urls import path
from . import views

app_name = "stamps"

urlpatterns = [
    path(
        "students/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "student/qr/",
        views.student_qr,
        name="student_qr"
    ),
]