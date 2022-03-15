from django.urls import path

from . import views

urlpatterns = [
    path('get_recipe', views.get_recipe, name='get_recipe'),
]