from django.urls import path

from . import views

app_name = "activities"

urlpatterns = [
    path("", views.activity_list, name="list"),
    path("<int:pk>/edit/", views.activity_edit, name="edit"),
]
