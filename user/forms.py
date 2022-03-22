from django import forms
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'herbs', 'spices', 'proteins', 'vegetables', 'favorite', 'ban']
