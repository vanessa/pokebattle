from django import forms

from battles.helpers.battle import check_run_battle_and_return_winner
from battles.helpers.emails import send_email_when_battle_finishes
from pokemons.helpers import check_if_pokemon_stats_exceeds_600, create_pokemon_if_not_exists
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

        first_pokemon = cleaned_data.get('first_pokemon')
        second_pokemon = cleaned_data.get('second_pokemon')
        third_pokemon = cleaned_data.get('third_pokemon')

        battle = self.initial['battle_related']

        if not first_pokemon:
            raise forms.ValidationError(
                'Invalid input. Please, use numbers only.'
            )

        if not second_pokemon:
            raise forms.ValidationError(
                'Invalid input. Please, use numbers only.'
            )

        if not third_pokemon:
            raise forms.ValidationError(
                'Invalid input. Please, use numbers only.'
            )

        if str(first_pokemon).startswith('0'):
            raise forms.ValidationError(
                'Pokemon\'s id cannot start with 0!'
            )

        if str(second_pokemon).startswith('0'):
            raise forms.ValidationError(
                'Pokemon\'s id cannot start with 0!'
            )

        if str(third_pokemon).startswith('0'):
            raise forms.ValidationError(
                'Pokemon\'s id cannot start with 0!'
            )

        pokemon_list = []
        pokemon_list.extend([
            first_pokemon,
            second_pokemon,
            third_pokemon
        ])

        if len(set(pokemon_list)) != 3:
            raise forms.ValidationError(
                'There are duplicates Pokemon, please use unique ids'
            )

        for pokemon in pokemon_list:
            create_pokemon_if_not_exists(pokemon)

        if check_if_pokemon_stats_exceeds_600(pokemon_list) is True:
            raise forms.ValidationError(
                'Your Pokemon stats cannot sum more than 600.'
            )

        new_team = BattleTeam.objects.create(
            battle_related=battle,
            trainer=self.initial['trainer'],
        )
        new_team.pokemons.add(*Pokemon.objects.filter(id__in=pokemon_list))

        battle_winner = check_run_battle_and_return_winner(battle.id)

        if battle_winner:
            battle.winner = battle_winner
            battle.save()
            send_email_when_battle_finishes(battle.id)

        return cleaned_data
