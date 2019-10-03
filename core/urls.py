from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('speaker-details', views.speaker_details),
]
