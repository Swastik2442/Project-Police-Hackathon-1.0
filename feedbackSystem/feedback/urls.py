from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="feedbackIndex"),
    path("submit/", views.submitFeedback_view, name="feedbackSubmit"),
    path("submitted/", views.submittedFeedbacks_view, name="feedbackView"),
    path("api/getStations", views.getStations_api, name="APIstations"),
]