from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['id', 'cooking_method', 'cuisine', 'image', 'ingredients', 'name', 'prep_time', 'tags']
