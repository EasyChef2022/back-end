from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['id', 'cook_time', 'prep_time', 'description', 'ingredients', 'instructions', 'photo_url',
                  'rating', 'title', 'recipe_url']
