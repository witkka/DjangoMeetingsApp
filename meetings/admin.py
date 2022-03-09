"""
Configuration necessary for registering models at the automatic admin interface.
It reads metadata from models to provide a quick, model-centric interface where
trusted users can manage content on this site.
"""
from django.contrib import admin
from meetings.models import Meeting

admin.site.register(Meeting)

