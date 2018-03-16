from django import forms
from django.core.exceptions import ValidationError
from .models import Battle


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['opponent']

    first_pokemon = forms.CharField(required=True, label='Insert first Pokemon ID')
    second_pokemon = forms.CharField(required=True, label='Insert second Pokemon ID')
    third_pokemon = forms.CharField(required=True, label='Insert third Pokemon ID')

    def clean(self, **kwargs):
        cd = super().clean() # cd = short for cleaned data
        return cd