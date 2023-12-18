from django.shortcuts import render
from django.http import HttpRequest
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Division, PoliceStation, Feedback

def index_view(request: HttpRequest):
    """A Django View for the User Dashboard."""
    feedbacks = None
    search = request.GET.get('search', '')
    if search == '':
        feedbacks = Feedback.objects.all().order_by("-feedbackDate", "-reportedDate", "-incidentDate")
    else:
        feedbacks = Feedback.objects.filter(name__contains=search).order_by("-feedbackDate", "-reportedDate", "-incidentDate")
    page = request.GET.get('page', 1)
    paginator = Paginator(feedbacks, 10)
    try:
        details = paginator.page(page)
    except PageNotAnInteger:
        details = paginator.page(1)
    except EmptyPage:
        details = paginator.page(paginator.num_pages)
    return render(request, 'feedback/index.html', {"details": details, 'search': search})

def submitFeedback_view(request: HttpRequest):
    """A Django View for Submission of New Feedback."""
    return render(request, 'feedback/submit.html')

def reviewFeedback_view(request: HttpRequest, id: int):
    """A Django View for Reviewing Submitted Feedback."""
    return render(request, 'feedback/review.html')

def submittedFeedbacks_view(request: HttpRequest):
    """A Django View for Listing all Submitted Feedbacks."""
    return render(request, 'feedback/feedbacks.html')

def getStations_api(request: HttpRequest):
    """A Django View for Getting all Police Stations within a Division."""
    if request.method == "GET":
        divisionID = request.GET.get('divisionID', -1)
        if divisionID != -1:
            division = Division.objects.filter(id=divisionID).first()
            stations = PoliceStation.objects.filter(division=division)
            json = {"stations": list()}
            for i in stations:
                station = [i.id, i.name]
                json['stations'].append(station)
            return JsonResponse(json)
    return JsonResponse({'error': True})