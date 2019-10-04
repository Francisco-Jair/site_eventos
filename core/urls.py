from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('detalhes-palestrante/', views.detalhes_palestrante),
    path('inscricao', views.inscricao),
]
