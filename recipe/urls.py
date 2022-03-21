from django.urls import path

from . import views

urlpatterns = [
    path('get_recipe_by_ingredients', views.get_recipe_by_ingredients, name='get_recipe_by_ingredients'),
    path('get_recipe_by_ingredients', views.get_recipe_by_name, name='get_recipe_by_name'),
]
