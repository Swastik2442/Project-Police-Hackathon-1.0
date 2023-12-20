from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="accessIndex"),
    path("test/", views.test_view, name="accessTest"),
]