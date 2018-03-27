import json

from django import forms

import requests as r

from pokemons.models import Pokemon
from users.models import User

from .models import Battle, BattleTeam
from .variables import POKEMON_URL


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['creator', 'opponent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.exclude(id=self.initial['creator'].id)
        self.fields['opponent'] = forms.ModelChoiceField(
            queryset=users
        )

    def clean(self, **kwargs):
        return super().clean()


class ChooseTeamForm(forms.ModelForm):
    class Meta:
        model = BattleTeam
        fields = ['battle_related', 'trainer']

    first_pokemon = forms.CharField(required=True, label='First pokemon')
    second_pokemon = forms.CharField(required=True, label='Second pokemon')
    third_pokemon = forms.CharField(required=True, label='Third pokemon')

    def clean(self, **kwargs):
        cleaned_data = super().clean()

        if (not cleaned_data['first_pokemon'].isdigit() or
            not cleaned_data['second_pokemon'].isdigit() or
            not cleaned_data['third_pokemon'].isdigit()):
            raise forms.ValidationError(
                'Sorry, we only accept Pokemons ids!'
            )
        pokemon_list = []
        pokemon_list.extend([
            cleaned_data['first_pokemon'],
            cleaned_data['second_pokemon'],
            cleaned_data['third_pokemon']
        ])

        for pokemon in pokemon_list:
            try:
                pokemon = Pokemon.objects.get(id=pokemon)
            except Pokemon.DoesNotExist:
                result = r.get('{}/{}'.format(POKEMON_URL, str(pokemon)))
                result = json.loads(result.text)
                new_pokemon = Pokemon(
                    id=pokemon,
                    name=result['name'],
                    sprite=result['sprites']['front_default']
                )
                stats = [(stats['stat']['name'], stats['base_stat'])
                         for stats in result['stats']]
                stats_obj = {}
                for stat in stats:
                    stat_name = stat[0]
                    stat_value = stat[1]
                    if (stat_name == 'defense' or
                        stat_name == 'attack' or
                            stat_name == 'hp'):
                        stats_obj[stat_name] = stat_value
                new_pokemon.defense = stats_obj['defense']
                new_pokemon.attack = stats_obj['attack']
                new_pokemon.hp = stats_obj['hp']
                new_pokemon.save()
        new_team = BattleTeam.objects.create(
            battle_related=cleaned_data['battle_related'],
            trainer=cleaned_data['trainer'],
        )
        new_team.pokemons.add(*Pokemon.objects.filter(id__in=pokemon_list))
        return cleaned_data