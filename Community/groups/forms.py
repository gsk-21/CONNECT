from django import forms
from .models import Group


class GroupChangeListForm(forms.ModelForm):

    members = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
