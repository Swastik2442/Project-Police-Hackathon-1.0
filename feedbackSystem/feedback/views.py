from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import AnonymousUser
from django.utils.timezone import make_aware

from feedbackSystem.settings import LANGUAGE_CODE
from base.messaging import MessageHandler
from .utils import getMessageFromFeedback
from .models import Division, PoliceStation, Feedback

jsTimeFormat = "%Y-%m-%dT%H:%M"

def index_view(request: HttpRequest):
    """A Django View for the User Dashboard."""
    feedbacks = None
    feedbacks = Feedback.objects.all().order_by("-feedbackDate", "-reportedDate", "-incidentDate")
    page = request.GET.get('page', 1)
    paginator = Paginator(feedbacks, 10)
    try:
        details = paginator.page(page)
    except PageNotAnInteger:
        details = paginator.page(1)
    except EmptyPage:
        details = paginator.page(paginator.num_pages)
    return render(request, 'feedback/index.html', {"details": details})

def submitFeedback_view(request: HttpRequest):
    """A Django View for Submission of New Feedback."""
    context = dict()
    divisions = Division.objects.all()
    context['divisions'] = divisions
    if request.method == 'POST':
        userIP = request.META.get('REMOTE_ADDR')
        stationID = request.POST.get('stationID')
        experience = request.POST.get('experience')
        description = request.POST.get('description')
        feedbackDate = make_aware(datetime.now())

        incidentDate = request.POST.get('incidentDate', '')
        reportedDate = request.POST.get('reportedDate', '')
        if incidentDate == '':
            incidentDate = None
        else:
            incidentDate = make_aware(datetime.strptime(incidentDate, jsTimeFormat))
        if reportedDate == '':
            reportedDate = None
        else:
            reportedDate = make_aware(datetime.strptime(reportedDate, jsTimeFormat))
        
        user = request.user
        if isinstance(user, AnonymousUser):
            user = None

        try:
            station = PoliceStation.objects.get(id=stationID)
            new = Feedback(
                submittedBy=user,
                userIP=userIP,
                forStation=station,
                experience=experience,
                description=description,
                incidentDate=incidentDate,
                reportedDate=reportedDate,
                feedbackDate=feedbackDate
                )
            new.save()
            if user != None and user.get_username().isdigit():
                message = getMessageFromFeedback(new, request.COOKIES.get('django_language', LANGUAGE_CODE))
                MessageHandler(user.get_username()).sendMessage(message)
            return redirect(request.GET.get("next", "feedbackView"))
        except Exception as err:
            print(err)
            context['error'] = True
            return render(request, 'feedback/submit.html', context)
    return render(request, 'feedback/submit.html', context)

def submittedFeedbacks_view(request: HttpRequest):
    """A Django View for Listing all Submitted Feedbacks."""
    if request.user.is_authenticated:
        feedbacks = Feedback.objects.filter(submittedBy=request.user).order_by("-feedbackDate", "-reportedDate", "-incidentDate")
        page = request.GET.get('page', 1)
        paginator = Paginator(feedbacks, 10)
        try:
            details = paginator.page(page)
        except PageNotAnInteger:
            details = paginator.page(1)
        except EmptyPage:
            details = paginator.page(paginator.num_pages)
        return render(request, 'feedback/view.html', {'feedbacks': details})
    return render(request, 'feedback/view.html')

def getStations_api(request: HttpRequest):
    """A Django View for Getting all Police Stations within a Division."""
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