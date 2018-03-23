from django import forms
from django.core.exceptions import ValidationError

from pokemons.models import Pokemon
from users.models import User

from .models import Battle, BattleTeam


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['creator', 'opponent'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.exclude(id=self.initial['creator'].id)
        self.fields['opponent'] = forms.ModelChoiceField(
            queryset = users
        )

    def clean(self, **kwargs):
        return super().clean()

class ChooseTeamForm(forms.ModelForm):
    class Meta:
        model = BattleTeam
        fields = []

    first_pokemon = forms.CharField(required=True, label='Insert first Pokemon ID')
    second_pokemon = forms.CharField(required=True, label='Insert second Pokemon ID')
    third_pokemon = forms.CharField(required=True, label='Insert third Pokemon ID')

    def clean(self, **kwargs):
        print(self)
        return super().clean()
