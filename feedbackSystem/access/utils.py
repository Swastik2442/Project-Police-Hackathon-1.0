from calendar import month_name
from time import localtime, mktime

from django.db import connection

from feedback.models import Feedback, PoliceStation

def getLast12Months():
    now = localtime()
    last12months = [localtime(mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(12)]
    x = 0
    for i in last12months:
        last12months[x] = month_name[i[1]] + ' ' + str(i[0])
        x += 1
    return last12months

def getTopStationsByNoOfFeedbacks(n: int):
    stations = None
    cursor = connection.cursor()
    cursor.execute("SELECT forStation_id, COUNT(*) AS counter FROM feedback_Feedback GROUP BY forStation_id ORDER BY counter DESC LIMIT %s;", [n])
    stations = cursor.fetchall()
    x = 0
    for i in stations:
        stationID = i[0]
        cursor.execute("SELECT COUNT(*) FROM feedback_Feedback WHERE forStation_id = %s AND experience > 3;", [stationID])
        positives = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM feedback_Feedback WHERE forStation_id = %s AND experience = 3;", [stationID])
        neutrals = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM feedback_Feedback WHERE forStation_id = %s AND experience < 3;", [stationID])
        negatives = cursor.fetchone()[0]
        station = PoliceStation.objects.get(id=stationID)
        stations[x] = [station.name, i[1], positives, neutrals, negatives]
        x += 1
    return stations