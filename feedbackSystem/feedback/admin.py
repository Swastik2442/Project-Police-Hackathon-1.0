from django.contrib import admin

from .models import Division, PoliceStation

class DivisionAdmin(admin.ModelAdmin):
    list_display = ["name", "state"]

class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ["name", "division"]

admin.site.register(Division, DivisionAdmin)
admin.site.register(PoliceStation, PoliceStationAdmin)