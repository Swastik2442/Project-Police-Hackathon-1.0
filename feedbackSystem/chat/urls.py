from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="chatIndex"),
    path("api/addMessage/<int:chatID>", views.addMessage_API, name="APIaddMessage"),
]