"""
Configuration for the views.py of the 'meetings' app necessary to take web requests and return a web response.
"""
from django.shortcuts import render, get_object_or_404, redirect
from .models import Meeting, Room
from .forms import MeetingForm
import re
from django.contrib import messages
from django.utils import timezone


def index(request, id):
    """
    This method is responsible for taking id number of a particular meeting, collecting data from database and
    connecting view with template 'index.html', and rendering page content.

    Parameters
    ----------
    request: request object
    id: int
        this parameter is a unique id number of a meeting

    Returns
    -------
    request object
    html template
    context containing data of a particular meeting with given id number
    """
    meeting = get_object_or_404(Meeting, pk=id)
    return render(request, "meetings/index.html", {"meeting": meeting})


def new(request):
    """
    This method is responsible for creating new entry in the database based on data collected from the form.
    Data can be submitted only by a logged in user that is the author of this meeting. All data, except for
    username, which is filled in automatically, must be entered by the user.
    If correct data is submitted, the user is redirected to the index page.
    """
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            meeting = form.save()
            return redirect("index", id=meeting.pk)
    else:
        form = MeetingForm()
    return render(request, "meetings/new.html", {"form": form})


def home(request):
    """Method responsible for creating home page.
    For logged-in users displays all future meetings and main menu.
    For not logged users, displays main menu and message."""
    if request.user.is_authenticated:
        user_meetings = Meeting.objects.meetings_for_user(request.user)

        meetings_today = user_meetings.filter(date=timezone.datetime.today())
        meetings_future = user_meetings.filter(date=timezone.datetime.today())
        context = {"meetings_today": meetings_today, "meetings_future": meetings_future}
        return render(request, "meetings/home.html", context)
    else:
        return render(request, "meetings/home.html")


def is_valid_queryparam(param):
    """Helper function to check if entered query parameters are valid."""
    return param != "" and param is not None


def get_room_elements(room):
    """Helper function for collecting data from the form."""
    return (
        re.split("number: |, |floor: ", room)[-3],
        re.split("number: |, |floor: ", room)[-1],
    )


def search_form(request):
    """
    Function responsible for displaying sear form page, collecting data from the form
    and displaying query results.
    """
    qs = Meeting.objects.all()
    rooms = Room.objects.all()
    if request.method == "GET":
        title_contains_query = request.GET.get("title_contains")
        author_query = request.GET.get("author")
        date_min_query = request.GET.get("date_min")
        date_max_query = request.GET.get("date_max")
        room_query = request.GET.get("room")
        time_min_query = request.GET.get("time_min")
        time_max_query = request.GET.get("time_max")
        if is_valid_queryparam(title_contains_query):
            qs = qs.filter(title__icontains=title_contains_query)

        if is_valid_queryparam(author_query):
            qs = qs.filter(author__username__icontains=author_query)

        if is_valid_queryparam(date_min_query):
            qs = qs.filter(date__gte=date_min_query)

        if is_valid_queryparam(date_max_query):
            qs = qs.filter(date__lte=date_max_query)

        if is_valid_queryparam(room_query) and room_query != "Choose room!":
            number, floor = get_room_elements(room_query)
            qs = qs.filter(room__number=number).filter(room__floor=floor)

        if is_valid_queryparam(time_min_query):
            qs = qs.filter(start_time__gte=time_min_query)

        if is_valid_queryparam(time_max_query):
            qs = qs.filter(end_time__lte=time_max_query)

        return render(
            request,
            "meetings/search_form.html",
            context={"queryset": qs, "rooms": rooms},
        )


def edit_object(request, id):
    """Method responsible for editing displaying page for data in the database and
    editing data.
    If chosen meeting cannot be changed, a message is displayed."""
    obj = Meeting.objects.get(id=id)
    form = MeetingForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.instance.author = request.user
        meeting = form.save()
        messages.success(request, "Meeting changed.")
        return redirect("index", id=meeting.pk)
    else:
        context = {"form": form, "error": "Meeting could not be changed."}
        return render(request, "meetings/edit.html", context)


def delete_object(request, id):
    """Method responsible for displaying delete page and deleting meeting from the database."""
    meeting = Meeting.objects.get(id=id)
    if request.method == "POST":
        meeting.delete()
        return redirect("confirmation")
    return render(request, "meetings/delete.html", context={"meeting": meeting})


def confirm_delete(request):
    """Method responsible for rendering confirmation page with information, that given meeeting has been deleted."""
    return render(request, "meetings/confirmation.html")
