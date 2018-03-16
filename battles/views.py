from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import pokebase as pb

from pokemons.models import Pokemon
from .models import ChosenPokemons

from .forms import CreateBattleForm


class BattlesListView(generic.TemplateView):
    template_name = 'battles/battles_list.html'

class CreateBattleView(generic.CreateView):
    template_name = 'battles/create_battle.html'
    form_class = CreateBattleForm

    def get_success_url(self):
        return reverse('battles:create-battle')

    def form_valid(self, form):
        data = form.instance
        data.creator = self.request.user
        pokemons = []
        pokemons.extend([
            form.cleaned_data['first_pokemon'],
            form.cleaned_data['second_pokemon'],
            form.cleaned_data['third_pokemon']
        ])
        for pokemon_id in pokemons:
            try:
                query = Pokemon.objects.get(id=pokemon_id)
            except Pokemon.DoesNotExist:
                pkn = pb.pokemon(pokemon_id)
                new_pokemon = Pokemon(
                    id = pokemon_id,
                    name = pkn.name,
                    attack = '1',
                    defense = '2',
                    hp = '3'
                )
                new_pokemon.save()
        chosen_pokemons = ChosenPokemons(
            battle_related = self.object,
            first = Pokemon.objects.get(id=pokemons[0]),
            second = Pokemon.objects.get(id=pokemons[1]),
            third = Pokemon.objects.get(id=pokemons[2]),
            trainer = data.creator
        )
        return super().form_valid(form)