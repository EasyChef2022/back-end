from django.urls import path

from . import views

urlpatterns = [
    path('sign_up', views.user_sign_up, name='create_user'),
    path('sign_in', views.user_sign_in, name='sign_in'),
    path('change_password', views.user_change_password, name='change_password'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('add_pantry', views.user_add_pantry, name='add_pantry'),
    path('remove_pantry', views.user_remove_pantry, name='remove_pantry'),
    path('get_user', views.get_user_by_username, name='get_user')
]
