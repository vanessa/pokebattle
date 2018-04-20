from django import forms

from pokemons.helpers import check_if_pokemon_stats_exceeds_600, init_pokemon_object
from pokemons.models import Pokemon
from users.models import User

from .helpers import check_and_run_battle, has_team_duplicate_pokemon
from .models import Battle, BattleTeam


class CreateBattleForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = ['opponent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.exclude(id=self.initial['creator'])
        self.fields['opponent'].queryset = users


def validate_integer_doesnt_start_with_zero(value):
    if str(value).startswith('0'):
        raise forms.ValidationError(
            'Your Pokemon id ({pokemon_id}) cannot start with 0.'.format(
                pokemon_id=value
            )
        )


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

        team = [first_pokemon, second_pokemon, third_pokemon]

        if has_team_duplicate_pokemon(team):
            raise forms.ValidationError(
                'There are duplicates Pokemon, please use unique ids.'
            )

        if check_if_pokemon_stats_exceeds_600([first_pokemon, second_pokemon,
                                               third_pokemon]):
            raise forms.ValidationError(
                'Your Pokemon stats cannot sum more than 600.'
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
            battle_related=self.initial.get('battle_related'),
            trainer=self.initial.get('trainer'),
        )
        new_team.pokemons.add(
            *Pokemon.objects.filter(id__in=[pokemon.id for pokemon in pokemon_list]))
        check_and_run_battle(self.initial['battle_related'])
