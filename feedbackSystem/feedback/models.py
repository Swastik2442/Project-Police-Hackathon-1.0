from django.db import models
from django.contrib.auth.models import User
from macaddress.fields import MACAddressField

class Division(models.Model):
    """A Django Model representing a Police Division in a State."""
    name = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)

class PoliceStation(models.Model):
    """A Django Model representing a Police Station in a Division."""
    name = models.CharField(max_length=50, blank=False, null=False)
    division = models.ForeignKey(Division, on_delete=models.RESTRICT, blank=False, null=False)

class Feedback(models.Model):
    """A Django Model representing a Feedback entered by a User."""
    submittedBy = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True, blank=False)
    userMAC = MACAddressField(blank=False, null=False, integer=False)

    forStation = models.ForeignKey(PoliceStation, on_delete=models.RESTRICT, default=None, null=False, blank=False)
    description = models.TextField(max_length=500, blank=False, null=False)

    incidentDate = models.DateTimeField(blank=True, null=True)
    reportedDate = models.DateTimeField(blank=False, null=False)
    feedbackDate = models.DateTimeField(blank=False, null=False)