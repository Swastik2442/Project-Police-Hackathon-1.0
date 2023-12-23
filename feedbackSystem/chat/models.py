from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    """A Django Model representing the Chat with a User."""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    userIP = models.GenericIPAddressField(blank=False, null=False)

class Message(models.Model):
    """A Django Model representing a Message in a Chat."""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    byBot = models.BooleanField(default=False, blank=False, null=False)
    discussionEnd = models.BooleanField(default=False, blank=False, null=False)