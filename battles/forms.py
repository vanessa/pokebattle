from django import forms

from pokemons.helpers import create_pokemon_if_not_exists
from pokemons.models import Pokemon
from users.models import User

from .models import Battle, BattleTeam


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['opponent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.exclude(id=self.initial['creator'])
        self.fields['opponent'].queryset = users


class ChooseTeamForm(forms.ModelForm):
    class Meta:
        model = BattleTeam
        fields = []

    first_pokemon = forms.IntegerField(
        min_value=1, max_value=802, required=True, label='First pokemon')
    second_pokemon = forms.IntegerField(
        min_value=1, max_value=802, required=True, label='Second pokemon')
    third_pokemon = forms.IntegerField(
        min_value=1, max_value=802, required=True, label='Third pokemon')

    def clean(self):
        cleaned_data = super().clean()

        pokemon_list = []
        pokemon_list.extend([
            cleaned_data['first_pokemon'],
            cleaned_data['second_pokemon'],
            cleaned_data['third_pokemon']
        ])

        for pokemon in pokemon_list:
            create_pokemon_if_not_exists(pokemon)
        new_team = BattleTeam.objects.create(
            battle_related=self.initial['battle_related'],
            trainer=self.initial['trainer'],
        )
        new_team.pokemons.add(*Pokemon.objects.filter(id__in=pokemon_list))
        return cleaned_data
