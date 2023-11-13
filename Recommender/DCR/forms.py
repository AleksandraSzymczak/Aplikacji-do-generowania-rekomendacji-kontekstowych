from django import forms
from .models import UserChoices

class UserChoicesForm(forms.ModelForm):
    class Meta:
        model = UserChoices
        fields = [
            'c1_choices', 'selection_type_c1',
            'c2_choices', 'selection_type_c2',
            'c3_choices', 'selection_type_c3',
        ]