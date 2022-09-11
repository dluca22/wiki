from django.urls import path

from . import views

app_name='wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("<str:entry>/", views.entry, name="entry"),
    path("create", views.create, name="create"),
]
