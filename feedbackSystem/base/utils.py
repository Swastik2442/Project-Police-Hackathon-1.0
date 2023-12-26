import csv

from django.contrib.auth.models import Group

from feedback.models import Division, PoliceStation

requiredGroups = ['policeStaff', 'authVerified', 'authNotVerified']

def initialSetup(divisionDataFile: str, stationDataFile: str):
    """Function to setup the Project initially.

    `divisionDataFile` - CSV File with Field Names: `id`, `ename`, `hname`, `state`
    `stationDataFile` - CSV File with Field Names: `id`, `did`, `dname`, `sname`"""

    if not Group.objects.all().exists():
        for i in requiredGroups:
            grp = Group.objects.create(name=i)
            grp.save()

    if not Division.objects.all().exists():
        with open(divisionDataFile, 'r', encoding='utf-8') as file:
            parser = csv.DictReader(file)
            for i in parser:
                div = Division.objects.create(name=i['ename'], state=i['state'])
                div.save()

    if not PoliceStation.objects.all().exists():
        with open(stationDataFile, 'r', encoding='utf-8') as file:
            parser = csv.DictReader(file)
            for i in parser:
                div = Division.objects.get(name=i['dname'])
                station = PoliceStation.objects.create(name=i['sname'], division=div)
                station.save()