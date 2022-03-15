from django.urls import path

from . import views

urlpatterns = [
    path('sign_up', views.user_sign_up, name='create_user'),
    path('sign_in', views.user_sign_in, name='sign_in'),
    path('change_password', views.user_change_password, name='change_password'),
]
