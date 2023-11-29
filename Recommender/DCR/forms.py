from django import forms
from .models import UserChoices


class UserChoicesForm(forms.ModelForm):
    class Meta:
        model = UserChoices
        fields = [
            'c1_choices',
            'c2_choices',
            'c3_choices',
        ]
        widgets = {
            'c1_choices': forms.CheckboxSelectMultiple,
            'c2_choices': forms.CheckboxSelectMultiple,
            'c3_choices': forms.CheckboxSelectMultiple,
        }
        required = {
            'c1_choices': False,
            'c2_choices': False,
            'c3_choices': False,
        }