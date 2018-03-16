from django import forms

from .models import Battle


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['opponent']

    first_pokemon = forms.CharField(required=True, label='Insert first Pokemon ID')
    second_pokemon = forms.CharField(required=True, label='Insert second Pokemon ID')
    third_pokemon = forms.CharField(required=True, label='Insert third Pokemon ID')

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
