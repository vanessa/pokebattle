from django import forms

from dal import autocomplete

from battles.helpers.battle import can_teams_battle
from pokemons.helpers import has_team_duplicate_pokemon, pokemon_stats_exceeds_limit
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

    first_pokemon = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='/battles/pokemon-autocomplete',
            attrs={
                'data-placeholder': 'Select the first Pokemon',
                'data-html': True
            })
    )

    second_pokemon = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='/battles/pokemon-autocomplete',
            attrs={
                'data-placeholder': 'Select the second Pokemon',
                'data-html': True
            })
    )

    third_pokemon = forms.ModelChoiceField(
        queryset=Pokemon.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='/battles/pokemon-autocomplete',
            attrs={
                'data-placeholder': 'Select the third Pokemon',
                'data-html': True
            })
    )

    def clean_first_pokemon(self):
        pokemon = self.cleaned_data.get('first_pokemon')
        return pokemon

    def clean_second_pokemon(self):
        pokemon = self.cleaned_data.get('second_pokemon')
        return pokemon

    def clean_third_pokemon(self):
        pokemon = self.cleaned_data.get('third_pokemon')
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
                'There are duplicate Pokemon, please use unique ids.'
            )

        if pokemon_stats_exceeds_limit(team):
            raise forms.ValidationError(
                'Your Pokemon stats cannot sum more than 600.'
            )

        existent_team_pokemon = BattleTeam.objects.filter(
            battle_related=battle_related
        ).first()

        if existent_team_pokemon and can_teams_battle(
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
        return new_team
