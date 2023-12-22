from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import user_passes_test

from .utils import *

last12Months = getLastMonths(12)
last3Months = [last12Months[-1], last12Months[-2], last12Months[-3]]

def isStaffMember(user):
    """Checks if Logged In User is a Staff Member."""
    return user.groups.filter(name='policeStaff').exists()

@user_passes_test(isStaffMember, '/login')
def index_view(request: HttpRequest):
    """A Django View for the Staff Dashboard."""
    dataset = list()
    for i in last12Months:
        month = i[0]
        year = int(i[1])
        feedbacks = getFeedbacksDuringTimePeriod(fromMonth=month, fromYear=year, toMonth=month, toYear=year)
        dataset.append(len(feedbacks))
    return render(request, 'access/index.html', {'last3Months': last3Months, 'labels': last12Months, 'dataset': dataset, 'stations': getTopStationsByNoOfFeedbacks(10)})

@user_passes_test(isStaffMember, '/login')
def users_view(request: HttpRequest):
    """A Django View for the Staff Dashboard Page analysing Users."""
    dataset = list()
    for i in last12Months:
        month = i[0]
        year = int(i[1])
        users = getUsersDuringTimePeriod(fromMonth=month, fromYear=year, toMonth=month, toYear=year)
        dataset.append(len(users))
    return render(request, 'access/users.html', {'last3Months': last3Months, 'labels': last12Months, 'dataset': dataset, 'users': getTopUsersByNoOfFeedbacks(10)})