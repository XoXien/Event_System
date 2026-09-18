from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from accounts.models import Profile
from events.models import Event
from stamps.models import EventStamp
from .models import Attendance
from .services import validate_qr_token

def _is_organizer(user):
    return hasattr(user, "profile") and user.profile.role == Profile.Role.ORGANIZER

@login_required
def scanner(request, event_id):
    if not _is_organizer(request.user):
        raise PermissionDenied
    event = get_object_or_404(Event, id=event_id)
    if event.organizer_id != request.user.id and not request.user.is_staff:
        raise PermissionDenied
    return render(request, "attendance/scanner.html", {"event": event})

@login_required
def scan_api(request, event_id):
    if request.method != "POST":
        return JsonResponse({"ok": False, "message": "POST required."}, status=405)

    if not _is_organizer(request.user):
        return JsonResponse({"ok": False, "message": "Organizer access required."}, status=403)

    event = get_object_or_404(Event, id=event_id)
    if event.organizer_id != request.user.id and not request.user.is_staff:
        return JsonResponse({"ok": False, "message": "You are not assigned to this event."}, status=403)

    token = request.POST.get("token", "").strip()
    scan_type = request.POST.get("scan_type", "").upper()

    if scan_type not in {"IN", "OUT"}:
        return JsonResponse({"ok": False, "message": "Invalid scan type."}, status=400)

    payload, error = validate_qr_token(token)
    if error:
        return JsonResponse({"ok": False, "message": error}, status=400)

    profile = Profile.objects.filter(user_id=payload.get("uid"), role=Profile.Role.STUDENT).select_related("user").first()
    if not profile:
        return JsonResponse({"ok": False, "message": "Student account not found."}, status=404)

    now = timezone.now()

    try:
        with transaction.atomic():
            attendance = (
                Attendance.objects
                .select_for_update()
                .filter(student=profile, event=event)
                .first()
            )

            if scan_type == "IN":
                if attendance and attendance.in_at:
                    return JsonResponse({
                        "ok": False,
                        "message": f"{profile.display_name} already has an IN scan.",
                        "student": profile.display_name,
                    }, status=409)

                if attendance is None:
                    attendance = Attendance(student=profile, event=event)

                attendance.in_at = now
                attendance.in_scanned_by = request.user
                attendance.save()

                return JsonResponse({
                    "ok": True,
                    "message": f"IN recorded for {profile.display_name}.",
                    "student": profile.display_name,
                    "student_id": profile.student_id,
                    "scan_type": "IN",
                    "time": timezone.localtime(now).strftime("%I:%M:%S %p"),
                })

            # OUT
            if attendance is None or not attendance.in_at:
                return JsonResponse({
                    "ok": False,
                    "message": f"{profile.display_name} has no valid IN scan for this event.",
                    "student": profile.display_name,
                }, status=409)

            if attendance.out_at:
                return JsonResponse({
                    "ok": False,
                    "message": f"{profile.display_name} already has an OUT scan.",
                    "student": profile.display_name,
                }, status=409)

            attendance.out_at = now
            attendance.out_scanned_by = request.user
            attendance.save()

            EventStamp.objects.get_or_create(student=profile, event=event)

            return JsonResponse({
                "ok": True,
                "message": f"OUT recorded. Stamp awarded to {profile.display_name}.",
                "student": profile.display_name,
                "student_id": profile.student_id,
                "scan_type": "OUT",
                "time": timezone.localtime(now).strftime("%I:%M:%S %p"),
                "stamp_awarded": True,
            })

    except IntegrityError:
        return JsonResponse({"ok": False, "message": "Attendance already exists."}, status=409)

@login_required
def attendance_list(request, event_id):
    if not _is_organizer(request.user):
        raise PermissionDenied
    event = get_object_or_404(Event, id=event_id)
    if event.organizer_id != request.user.id and not request.user.is_staff:
        raise PermissionDenied

    records = Attendance.objects.filter(event=event).select_related("student__user")
    return render(
        request,
        "attendance/attendance_list.html",
        {"event": event, "records": records},
    )
