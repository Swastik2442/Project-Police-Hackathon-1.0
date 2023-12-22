from calendar import isleap
from datetime import datetime
from time import localtime, mktime

from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.timezone import make_aware

from feedback.models import Feedback, PoliceStation

monthsItoN = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
monthsNtoI = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
shortMonthsI = (4, 6, 9, 11)
shortMonthsN = ('April', 'June', 'September', 'November')

def getLastMonths(n: int):
    """Returns the Last n Months from the Current Date."""
    now = localtime()
    lastmonths = [localtime(mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(n)]
    x = 0
    for i in lastmonths:
        lastmonths[x] = [monthsItoN[i[1]], str(i[0])]
        x += 1
    return list(reversed(lastmonths))

def getTopStationsByNoOfFeedbacks(n: int):
    """Returns the Top Police Stations with Station Name, No. of Feedbacks, Positive Experiences, Neutral Experiences and Negative Experiences."""
    stations = list(Feedback.objects.values('forStation').annotate(counter=Count('forStation')).order_by('-counter')[:n])
    x = 0
    for i in stations:
        stationID = i['forStation']
        station = PoliceStation.objects.get(id=stationID)
        positives = len(Feedback.objects.filter(forStation=station, experience__gt=3))
        neutrals = len(Feedback.objects.filter(forStation=station, experience=3))
        negatives = len(Feedback.objects.filter(forStation=station, experience__lt=3))
        stations[x] = [station.name, i['counter'], positives, neutrals, negatives]
        x += 1
    return stations

def getFeedbacksDuringTimePeriod(fromDay=1, fromMonth="January", fromYear=datetime.today().year, toDay=31, toMonth="December", toYear=datetime.today().year):
    """Returns the Feedbacks submitted during the provided time period."""
    if toMonth == 'February':
        if isleap(toYear):
            toDay = 29
        else:
            toDay = 28
    elif toMonth in shortMonthsN:
        toDay = 30

    fromTime = make_aware(datetime(fromYear, monthsNtoI[fromMonth], fromDay))
    toTime = make_aware(datetime(toYear, monthsNtoI[toMonth], toDay, 23, 59, 59))
    feedbacks = Feedback.objects.filter(feedbackDate__gte=fromTime, feedbackDate__lte=toTime)
    return feedbacks

def getTopUsersByNoOfFeedbacks(n: int):
    """Returns the Top Users with User Name, No. of Feedbacks, Positive Experiences, Neutral Experiences and Negative Experiences."""
    users = list(Feedback.objects.values('submittedBy').annotate(counter=Count('submittedBy')).order_by('-counter')[:n])
    x = 0
    for i in users:
        userID = i['submittedBy']
        user = User.objects.filter(id=userID).first()

        positives = len(Feedback.objects.filter(submittedBy=user, experience__gt=3))
        neutrals = len(Feedback.objects.filter(submittedBy=user, experience=3))
        negatives = len(Feedback.objects.filter(submittedBy=user, experience__lt=3))

        userName = 'Anonymous'
        if (user != None) and (user.first_name != ''):
            userName = user.first_name + ' ' + user.last_name

        users[x] = [userName, i['counter'], positives, neutrals, negatives]
        x += 1
    return users

def getUsersDuringTimePeriod(fromDay=1, fromMonth="January", fromYear=datetime.today().year, toDay=31, toMonth="December", toYear=datetime.today().year):
    """Returns the Non-Staff Users who created their accounts during the provided time period."""
    if toMonth == 'February':
        if isleap(toYear):
            toDay = 29
        else:
            toDay = 28
    elif toMonth in shortMonthsN:
        toDay = 30

    fromTime = make_aware(datetime(fromYear, monthsNtoI[fromMonth], fromDay))
    toTime = make_aware(datetime(toYear, monthsNtoI[toMonth], toDay, 23, 59, 59))
    users = User.objects.filter(date_joined__gte=fromTime, date_joined__lte=toTime, groups__name__contains='auth')
    return users