from django import forms

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
        return cleaned_data
