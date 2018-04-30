from django import forms

from battles.helpers.battle import teams_cannot_battle
from pokemons.helpers import (
    check_if_pokemon_stats_exceeds_600, has_team_duplicate_pokemon, init_pokemon_object
)
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

        first_pokemon = cleaned_data.get('first_pokemon')
        second_pokemon = cleaned_data.get('second_pokemon')
        third_pokemon = cleaned_data.get('third_pokemon')
        battle_related = self.initial.get('battle_related')

        team = [first_pokemon, second_pokemon, third_pokemon]

        if has_team_duplicate_pokemon(team):
            raise forms.ValidationError(
                'There are duplicates Pokemon, please use unique ids.'
            )

        if check_if_pokemon_stats_exceeds_600(team):
            raise forms.ValidationError(
                'Your Pokemon stats cannot sum more than 600.'
            )

        existent_team_pokemon = BattleTeam.objects.filter(
            battle_related=battle_related
        ).first()

        if existent_team_pokemon and teams_cannot_battle(
                existent_team_pokemon.pokemons.all(), team):
            raise forms.ValidationError(
                'Some of your Pokemon already exists in '
                'the opponent\'s team, please pick other ones.'
            )

        return cleaned_data

    def save(self, commit=True):
        first_pokemon = self.cleaned_data.get('first_pokemon')
        second_pokemon = self.cleaned_data.get('second_pokemon')
        third_pokemon = self.cleaned_data.get('third_pokemon')

        team = [first_pokemon, second_pokemon, third_pokemon]
        battle_related = self.initial.get('battle_related')
        trainer = self.initial.get('trainer')

        for pokemon in team:
            pokemon.save()

        new_team = BattleTeam.objects.create(
            battle_related=battle_related,
            trainer=trainer
        )
        new_team.pokemons.add(*team)
