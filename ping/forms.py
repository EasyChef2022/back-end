from django import forms
from .models import GroupMember


class GroupMemberForm(forms.ModelForm):
    class Meta:
        model = GroupMember
        fields = ['name', 'email']