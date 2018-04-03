from django import forms

from pokemons.models import Pokemon
from users.models import User

from .helpers import get_or_create_pokemon
from .models import Battle, BattleTeam


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

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['creator'] == cleaned_data['opponent']:
            raise forms.ValidationError(
                'You can\'t battle with yourself.'
            )
        return cleaned_data


class ChooseTeamForm(forms.ModelForm):
    class Meta:
        model = BattleTeam
        fields = ['battle_related', 'trainer']

    first_pokemon = forms.CharField(required=True, label='First pokemon')
    second_pokemon = forms.CharField(required=True, label='Second pokemon')
    third_pokemon = forms.CharField(required=True, label='Third pokemon')

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data['first_pokemon'].isdigit():
            raise forms.ValidationError(
                'Invalid input. Please, use numbers only.'
            )

        if not cleaned_data['second_pokemon'].isdigit():
            raise forms.ValidationError(
                'Invalid input. Please, use numbers only.'
            )

        if not cleaned_data['third_pokemon'].isdigit():
            raise forms.ValidationError(
                'Invalid input. Please, use numbers only.'
            )

        pokemon_list = []
        pokemon_list.extend([
            cleaned_data['first_pokemon'],
            cleaned_data['second_pokemon'],
            cleaned_data['third_pokemon']
        ])

        for pokemon in pokemon_list:
            get_or_create_pokemon(pokemon)
        new_team = BattleTeam.objects.create(
            battle_related=cleaned_data['battle_related'],
            trainer=cleaned_data['trainer'],
        )
        new_team.pokemons.add(*Pokemon.objects.filter(id__in=pokemon_list))
        return cleaned_data
