from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="accessIndex"),
    path("users/", views.users_view, name="accessUsers"),
]