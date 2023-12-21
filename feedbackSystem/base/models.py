import uuid

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """A Django Model to Handle OTPs per User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    otp = models.CharField(max_length=10, blank=False, null=False)
    uid = models.CharField(default=f'{uuid.uuid4}', max_length=200)