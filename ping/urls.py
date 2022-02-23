from django.urls import path

from . import views

urlpatterns = [
    path('', views.ping, name='ping'),
    path('add_member', views.create_group_member, name='add_member')
]