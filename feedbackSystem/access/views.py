from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import user_passes_test

from .utils import getLast12Months, getTopStationsByNoOfFeedbacks

def isStaffMember(user):
    """Checks if Logged In User is a Staff Member."""
    return user.groups.filter(name='policeStaff').exists()

testData = [10,200,3000,40,5000,600,7000,800,90,0,1100,120]

@user_passes_test(isStaffMember, '/login')
def index_view(request: HttpRequest):
    """A Django View for the Staff Dashboard."""
    return render(request, 'access/index.html', {'labels': getLast12Months(), 'dataset': testData, 'stations': getTopStationsByNoOfFeedbacks(10)})

@user_passes_test(isStaffMember, '/login')
def test_view(request: HttpRequest):
    """A Django View for the Staff Test."""
    return render(request, 'access/test.html')