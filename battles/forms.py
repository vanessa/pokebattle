from django import forms

from battles.helpers.battle import check_run_battle_and_save_winner, teams_cannot_battle
from pokemons.helpers import (
    check_if_pokemon_stats_exceeds_600, has_team_duplicate_pokemon, init_pokemon_object
)
from pokemons.models import Pokemon
from users.models import User

from .models import Battle, BattleTeam
from .validators import validate_integer_doesnt_start_with_zero


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
        min_value=1, max_value=802, required=True, label='First pokemon',
        validators=[validate_integer_doesnt_start_with_zero])
    second_pokemon = forms.IntegerField(
        min_value=1, max_value=802, required=True, label='Second pokemon',
        validators=[validate_integer_doesnt_start_with_zero])
    third_pokemon = forms.IntegerField(
        min_value=1, max_value=802, required=True, label='Third pokemon',
        validators=[validate_integer_doesnt_start_with_zero])

    def clean_first_pokemon(self):
        value = self.cleaned_data.get('first_pokemon')
        pokemon = init_pokemon_object(value)
        return pokemon

    def clean_second_pokemon(self):
        value = self.cleaned_data.get('second_pokemon')
        pokemon = init_pokemon_object(value)
        return pokemon

    def clean_third_pokemon(self):
        value = self.cleaned_data.get('third_pokemon')
        pokemon = init_pokemon_object(value)
        return pokemon

    def clean(self):
        cleaned_data = super().clean()

        # rw: try to have a pattern see that sometimes you call team, sometimes pokemons. (check the save method)
        first_pokemon = cleaned_data.get('first_pokemon')
        second_pokemon = cleaned_data.get('second_pokemon')
        third_pokemon = cleaned_data.get('third_pokemon')

        team = [first_pokemon, second_pokemon, third_pokemon]

        if has_team_duplicate_pokemon(team):
            raise forms.ValidationError(
                'There are duplicates Pokemon, please use unique ids.'
            )

        if check_if_pokemon_stats_exceeds_600(team):
            raise forms.ValidationError(
                'Your Pokemon stats cannot sum more than 600.'
            )

        # rw: use prefetch related for pokemons.
        existent_team_pokemon = BattleTeam.objects.filter(
            battle_related=self.initial.get('battle_related')  # rw: put it in a variable before(optional).
        ).first()

        # rw: you can use an and here, to avoid not needed nested ifs.
        if existent_team_pokemon:
            if teams_cannot_battle(existent_team_pokemon.pokemons.all(), team):
                raise forms.ValidationError(
                    'Some of your Pokemon already exists in '
                    'the opponent\'s team, please pick other ones.'
                )

        return cleaned_data

    def save(self, commit=True):
        pokemon_list = [
            self.cleaned_data.get('first_pokemon'),
            self.cleaned_data.get('second_pokemon'),
            self.cleaned_data.get('third_pokemon')
        ]

        for pokemon in pokemon_list:
            pokemon.save()

        new_team = BattleTeam.objects.create(
            battle_related=self.initial.get('battle_related'),  # rw: put in a variable, is better than repeat yourself.
            trainer=self.initial.get('trainer'),
        )
        # rw: i believe you can just pass the pokemon list here.
        new_team.pokemons.add(
            *Pokemon.objects.filter(id__in=[pokemon.id for pokemon in pokemon_list]))
        # rw: let's move this to form_valid at the view.
        check_run_battle_and_save_winner(self.initial['battle_related'])
