from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import pokebase as pb

from pokemons.models import Pokemon
from .models import (
    Battle,
    ChosenPokemon
)

from .forms import CreateBattleForm


class BattlesListView(generic.TemplateView):
    template_name = 'battles/battles_list.html'

class CreateBattleView(generic.CreateView):
    template_name = 'battles/create_battle.html'
    form_class = CreateBattleForm

    def get_success_url(self):
        return reverse('battles:details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
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
                    # TO-DO: Change
                    attack = '1',
                    defense = '2',
                    hp = '3'
                )
                new_pokemon.save()
            chosen_pokemon = ChosenPokemon(
                order = 1,
                battle_related = self.object,
                pokemon = Pokemon.objects.get(id=pokemon_id),
                trainer = form.instance.creator
            ).save()
        return super().form_valid(form)

class BattleView(generic.DetailView):
    model = Battle
    template_name = 'battles/battle.html'
    context_object_name = 'battle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['your_chosen_pokemons'] = ChosenPokemon.objects.filter(
            battle_related=self.object,
            trainer=self.request.user
            )
        context['opponent_chosen_pokemons'] = ChosenPokemon.objects.filter(
            battle_related=self.object,
            trainer=self.object.opponent
            )
        return context