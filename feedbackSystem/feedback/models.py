from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator

EXPERIENCE_CHOICES = models.IntegerChoices("Experience Choices", "1 2 3 4 5")

class Division(models.Model):
    """A Django Model representing a Police Division in a State."""
    name = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='division_unique_constraint',
                fields=['name', 'state'],
                violation_error_message="Division Name has to be Unique in that State"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.state})"

class PoliceStation(models.Model):
    """A Django Model representing a Police Station in a Division."""
    name = models.CharField(max_length=50, blank=False, null=False)
    division = models.ForeignKey(Division, on_delete=models.RESTRICT, blank=False, null=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='police_station_unique_constraint',
                fields=['name', 'division'],
                violation_error_message="Police Station Name has to be Unique in that Division"
            )
        ]

    def __str__(self):
        return f"{self.name}, {self.division}"

class Feedback(models.Model):
    """A Django Model representing a Feedback entered by a User."""
    submittedBy = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, blank=False, null=True)
    userIP = models.GenericIPAddressField(blank=False, null=False)

    forStation = models.ForeignKey(PoliceStation, on_delete=models.RESTRICT, default=None, blank=False, null=False)
    experience = models.PositiveSmallIntegerField(blank=False, null=False, choices=EXPERIENCE_CHOICES.choices, default=3)
    description = models.TextField(max_length=500, blank=False, null=False)

    incidentDate = models.DateTimeField(blank=False, null=True)
    reportedDate = models.DateTimeField(blank=False, null=True)
    feedbackDate = models.DateTimeField(blank=False, null=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='feedback_repetition_protection_constraint',
                fields=['submittedBy', 'feedbackDate'],
                violation_error_message="User cannot submit multiple Feedbacks at the same time"
            ),
            models.CheckConstraint(
                name='incidentDate_check_constraint',
                check=models.Q(incidentDate__isnull=True) | models.Q(incidentDate__lt=models.F('feedbackDate')),
                violation_error_message="Incident Date cannot be after Feedback Submission Date"
            ),
            models.CheckConstraint(
                name='reportedDate_check1_constraint',
                check=models.Q(reportedDate__isnull=True) | models.Q(reportedDate__lt=models.F('feedbackDate')),
                violation_error_message="Reported Date cannot be after Feedback Submission Date"
            ),
            models.CheckConstraint(
                name='reportedDate_check2_constraint',
                check=models.Q(reportedDate__isnull=True) | models.Q(reportedDate__gt=models.F('incidentDate')),
                violation_error_message="Reported Date cannot be before Incident Date"
            )
        ]

    def __str__(self):
        smallDescription = Truncator(self.description).chars(10)
        return f"{self.submittedBy}: {smallDescription} - {self.forStation}"