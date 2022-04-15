from django.urls import path

from . import views

urlpatterns = [
    path('', views.ping, name='ping'),
    path('ping', views.ping, name='ping')
]