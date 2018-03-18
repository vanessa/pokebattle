from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

# import pokebase as pb
import requests as r
import json

from .variables import POKEAPI_URL, POKEMON_URL

from pokemons.models import Pokemon

from .forms import (
    CreateBattleForm,
    ReplyBattleForm
)
from .models import Battle, ChosenPokemon


class BattlesListView(generic.TemplateView):
    template_name = 'battles/battles_list.html'

class CreateBattleView(generic.CreateView):
    model = Battle
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
                pkn = r.get(
                    POKEMON_URL + str(pokemon_id)
                    )
                pkn = json.loads(pkn.text)
                new_pokemon = Pokemon(
                    id = pokemon_id,
                    name = pkn['name'],
                    sprite = pkn['sprites']['front_default']
                )
                stats = [(stats['stat']['name'], stats['base_stat']) for stats in pkn['stats']]
                stats_list = {}
                for stat in stats:
                    stat_name = stat[0]
                    stat_value = stat[1]
                    if (stat_name == 'defense' or
                        stat_name == 'attack' or
                        stat_name == 'hp'):
                        stats_list[stat_name] = stat_value
                new_pokemon.defense = stats_list['defense']
                new_pokemon.attack = stats_list['attack']
                new_pokemon.hp = stats_list['hp']
                new_pokemon.save()
            chosen_pokemon = ChosenPokemon(
                order = int(pokemons.index(pokemon_id) + 1),
                battle_related = self.object,
                pokemon = Pokemon.objects.get(id=pokemon_id),
                trainer = self.request.user
            ).save()
        return super().form_valid(form)

class BattleView(generic.DetailView, generic.FormView):
    model = Battle
    template_name = 'battles/battle.html'
    context_object_name = 'battle'
    form_class = ReplyBattleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creator_chosen_pokemons'] = ChosenPokemon.objects.filter(
            battle_related=self.object,
            trainer=self.object.creator
            )
        context['opponent_chosen_pokemons'] = ChosenPokemon.objects.filter(
            battle_related=self.object,
            trainer=self.object.opponent
            )
        context['user_is_opponent'] = True if self.object.opponent == self.request.user else False
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('battles:details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = self.get_object()
        form.instance.pk = self.object.pk
        form.instance.creator = self.object.creator
        form.instance.opponent = self.object.opponent
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
                pkn = r.get(
                    POKEMON_URL + str(pokemon_id)
                )
                pkn = json.loads(pkn.text)
                new_pokemon = Pokemon(
                    id = pokemon_id,
                    name = pkn['name'],
                    sprite = pkn['sprites']['front_default']
                )
                stats = [(stats['stat']['name'], stats['base_stat']) for stats in pkn['stats']]
                stats_list = {}
                for stat in stats:
                    stat_name = stat[0]
                    stat_value = stat[1]
                    if (stat_name == 'defense' or
                        stat_name == 'attack' or
                        stat_name == 'hp'):
                        stats_list[stat_name] = stat_value
                new_pokemon.defense = stats_list['defense']
                new_pokemon.attack = stats_list['attack']
                new_pokemon.hp = stats_list['hp']
                new_pokemon.save()
            chosen_pokemon = ChosenPokemon(
                order = int(pokemons.index(pokemon_id) + 1),
                battle_related = self.object,
                pokemon = Pokemon.objects.get(id=pokemon_id),
                trainer = self.request.user
            ).save()
        return super().form_valid(form)