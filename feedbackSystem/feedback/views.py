from django.shortcuts import render
from django.http import HttpRequest

def index_view(request: HttpRequest):
    """The Django View for the User Dashboard."""
    return render(request, 'feedback/index.html')

def submitFeedback_view(request: HttpRequest):
    """The Django View for Submission of New Feedback."""
    return render(request, 'feedback/submit.html')

def reviewFeedback_view(request: HttpRequest, id: int):
    """The Django View for Reviewing Submitted Feedback."""
    return render(request, 'feedback/review.html')

def submittedFeedbacks_view(request: HttpRequest):
    """The Django View for Listing all Submitted Feedbacks."""
    return render(request, 'feedback/feedbacks.html')