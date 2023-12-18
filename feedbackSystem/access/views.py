from django.shortcuts import render
from django.http import HttpRequest

def index_view(request: HttpRequest):
    """A Django View for the Access Dashboard."""
    return render(request, 'access/index.html')