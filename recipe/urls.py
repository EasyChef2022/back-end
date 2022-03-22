from django.urls import path

from . import views

urlpatterns = [
    path('get_recipe_by_ingredients', views.get_recipe_by_ingredients, name='get_recipe_by_ingredients'),
    path('get_recipe_by_name', views.get_recipe_by_name, name='get_recipe_by_name'),
    path('get_recipe_by_id', views.get_recipe_by_id, name='get_recipe_by_id'),
    path('get_recipe_of_today', views.get_recipe_of_today, name='get_recipe_of_today'),
    path('add_recipe', views.add_recipe, name='add_recipe'),
]
