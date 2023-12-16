from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="feedbackIndex"),
    path("submit/", views.submitFeedback_view, name="feedbackSubmit"),
    path("review/<int:id>/", views.reviewFeedback_view, name="feedbackReview"),
    path("submitted/", views.submittedFeedbacks_view, name="feedbackReview"),
]