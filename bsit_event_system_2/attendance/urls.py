from django.urls import path
from . import views

app_name = "attendance"

urlpatterns = [
    path("event/<int:event_id>/scanner/", views.scanner, name="scanner"),
    path("event/<int:event_id>/scan/", views.scan_api, name="scan_api"),
    path("event/<int:event_id>/list/", views.attendance_list, name="attendance_list"),
]
