import io
import qrcode

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render

from accounts.models import Profile
from attendance.services import create_qr_token, qr_token_expiry
from .models import EventStamp

@login_required
def student_dashboard(request):
    profile = getattr(request.user, "profile", None)

    if not profile or profile.role != Profile.Role.STUDENT:
        raise PermissionDenied

    stamps = (
        EventStamp.objects
        .filter(student=profile)
        .select_related("event")
    )

    return render(
        request,
        "stamps/student_dashboard.html",
        {
            "profile": profile,
            "stamps": stamps,
        },
    )


@login_required
def student_qr(request):
    profile = getattr(request.user, "profile", None)

    if not profile or profile.role != Profile.Role.STUDENT:
        return HttpResponse(
            "Student access required.",
            status=403
        )

    # Create temporary QR token
    token = create_qr_token(profile)

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(token)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    # Convert QR image to PNG
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")

    response = HttpResponse(
        buffer.getvalue(),
        content_type="image/png"
    )

    # The QR token and countdown use the same server-side expiry boundary.
    expires_at = qr_token_expiry(token)
    response["X-QR-Expires-At"] = str(expires_at)

    # Prevent browser caching
    response["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, "
        "proxy-revalidate, max-age=0"
    )

    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response