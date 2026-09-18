from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from .forms import ProfileForm, StudentRegistrationForm
from .models import Profile


def student_login(request):
    """
    Login page specifically for student accounts.
    Only users with STUDENT role can log in here.
    """

    if request.user.is_authenticated:
        try:
            if request.user.profile.role == Profile.Role.STUDENT:
                return redirect("stamps:student_dashboard")
        except Profile.DoesNotExist:
            pass

        logout(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                profile = user.profile

                if profile.role != Profile.Role.STUDENT:
                    messages.error(
                        request,
                        "This login is for student accounts only."
                    )
                    return redirect("accounts:student_login")

            except Profile.DoesNotExist:
                messages.error(
                    request,
                    "Student profile not found."
                )
                return redirect("accounts:student_login")

            login(request, user)

            return redirect("stamps:student_dashboard")

        messages.error(
            request,
            "Invalid student username or password."
        )

    return render(
        request,
        "accounts/student_login.html"
    )


def organizer_login(request):
    """
    Login page specifically for organizer accounts.
    Only users with ORGANIZER role can log in here.
    """

    if request.user.is_authenticated:
        try:
            if request.user.profile.role == Profile.Role.ORGANIZER:
                return redirect("events:organizer_dashboard")
        except Profile.DoesNotExist:
            pass

        logout(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                profile = user.profile

                if profile.role != Profile.Role.ORGANIZER:
                    messages.error(
                        request,
                        "This login is for organizer accounts only."
                    )
                    return redirect("accounts:organizer_login")

            except Profile.DoesNotExist:
                messages.error(
                    request,
                    "Organizer profile not found."
                )
                return redirect("accounts:organizer_login")

            login(request, user)

            return redirect("events:organizer_dashboard")

        messages.error(
            request,
            "Invalid organizer username or password."
        )

    return render(
        request,
        "accounts/organizer_login.html"
    )


def register_student(request):
    """
    Public registration for student accounts only.
    """

    if request.user.is_authenticated:
        return redirect("stamps:student_dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                "Your student account has been created successfully."
            )

            login(request, user)

            return redirect("stamps:student_dashboard")

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


@login_required
def dashboard(request):
    """
    Sends the user to the correct dashboard based on role.
    """

    # Django superusers/admins do not need a Profile record.
    if request.user.is_staff:
        return redirect("/admin/")

    try:
        role = request.user.profile.role
    except Profile.DoesNotExist:
        logout(request)
        return redirect("accounts:student_login")

    if role == Profile.Role.STUDENT:
        return redirect("stamps:student_dashboard")

    elif role == Profile.Role.ORGANIZER:
        return redirect("events:organizer_dashboard")

    elif role == Profile.Role.ADMIN:
        return redirect("/admin/")

    logout(request)

    return redirect("accounts:student_login")


@login_required
def logout_view(request):

    # Remember the user's role before logging out
    try:
        role = request.user.profile.role
    except Profile.DoesNotExist:
        role = None

    logout(request)

    if role == Profile.Role.ORGANIZER:
        return redirect("accounts:organizer_login")

    if role == Profile.Role.STUDENT:
        return redirect("accounts:student_login")

    # Admin or unknown account
    return redirect("accounts:student_login")

@login_required
def profile(request):
    profile = getattr(request.user, "profile", None)

    if profile is None or profile.role != Profile.Role.STUDENT:
        raise PermissionDenied

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, "accounts/profile.html", {"form": form})
