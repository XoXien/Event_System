from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm
from .models import Event


def _is_organizer(user):
    return (
        hasattr(user, "profile")
        and user.profile.role == "ORGANIZER"
    )


@login_required
def organizer_dashboard(request):
    if not _is_organizer(request.user):
        raise PermissionDenied

    events = Event.objects.filter(
        organizer=request.user
    ).order_by("-date", "-start_time")

    return render(
        request,
        "events/organizer_dashboard.html",
        {"events": events}
    )


@login_required
def event_list(request):
    events = Event.objects.all().order_by(
        "-date",
        "-start_time"
    )

    return render(
        request,
        "events/event_list.html",
        {"events": events}
    )


@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    return render(
        request,
        "events/event_detail.html",
        {"event": event}
    )


@login_required
def event_create(request):

    # Only Admin or Organizer can create events
    if not request.user.is_staff and not _is_organizer(request.user):
        raise PermissionDenied

    form = EventForm(
        request.POST or None,
        request.FILES or None,
        user=request.user
    )

    if request.method == "POST" and form.is_valid():

        event = form.save(commit=False)

        # Organizer automatically becomes the event organizer
        if _is_organizer(request.user):
            event.organizer = request.user

        event.save()

        if _is_organizer(request.user):
            return redirect("events:organizer_dashboard")

        return redirect("events:event_list")

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "title": "Create Event"
        }
    )


@login_required
def event_edit(request, pk):

    event = get_object_or_404(Event, pk=pk)

    # Admin can edit any event
    # Organizer can only edit their own event
    if request.user.is_staff:
        pass
    elif _is_organizer(request.user) and event.organizer == request.user:
        pass
    else:
        raise PermissionDenied

    form = EventForm(
        request.POST or None,
        request.FILES or None,
        instance=event,
        user=request.user
    )

    if request.method == "POST" and form.is_valid():

        edited_event = form.save(commit=False)

        # Organizer cannot change ownership of their event
        if _is_organizer(request.user):
            edited_event.organizer = request.user

        edited_event.save()

        if _is_organizer(request.user):
            return redirect("events:organizer_dashboard")

        return redirect(
            "events:event_detail",
            pk=event.pk
        )

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "title": "Edit Event"
        }
    )