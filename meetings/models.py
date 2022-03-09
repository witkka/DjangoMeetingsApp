"""
Configuration of models.py of the meetings app necessary for creating
database and queryset.
"""
from datetime import time
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class Room(models.Model):
    """
    Class responsible for creating table 'Room' containing columns: name, number, floor.
    Class inherits from models.Model.
    """

    name = models.CharField(max_length=200)
    number = models.IntegerField()
    floor = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return f"Room: {self.name}, number: {self.number}, floor: {self.floor}"


class MeetingQuerySet(models.QuerySet):
    """
    Cass responsible for creating queryset filtering only those meetings where given
    user is a participant or author.
    """

    def meetings_for_user(self, user):
        """
        Method responsible for filtering only those meetings where given
        user is a participant or author.
        """
        return self.filter(Q(author=user) | Q(participants=user)).distinct()


class Meeting(models.Model):
    """Class responsible for creating table 'Meeting' containing columns:
    title, date, start_time, end_time, room, author and participants.
    Class inherits from models.Model."""

    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField(default=time(9))
    end_time = models.TimeField(default=time(17))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    participants = models.ManyToManyField(
        User, related_name="participants", null=True, blank=True
    )

    objects = MeetingQuerySet.as_manager()

    def __str__(self):
        return f"Meeting: {self.title} at: {self.start_time}"
