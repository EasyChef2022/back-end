from django.urls import path

from . import views

urlpatterns = [
    path('sign_up', views.create_user, name='create_user'),
]