import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

import requests as r

from pokemons.models import Pokemon

from .forms import ChooseTeamForm, CreateBattleForm
from .models import Battle, BattleTeam


class BattlesListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'battles/battles_list.html'


class CreateBattleView(LoginRequiredMixin, generic.CreateView):
    model = Battle
    template_name = 'battles/create_battle.html'
    form_class = CreateBattleForm

    def get_initial(self):
        return {'creator': self.request.user}

    def get_success_url(self):
        return reverse('battles:details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'creator': user
        })
        return context


class BattleView(LoginRequiredMixin, generic.DetailView):
    model = Battle
    template_name = 'battles/battle.html'
    context_object_name = 'battle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['creators_pokemons'] = BattleTeam.objects.get(
            battle_related=self.object,
            trainer=self.object.creator
            ).pokemons.all()
        context['opponents_pokemons'] = BattleTeam.objects.get(
            battle_related=self.object,
            trainer=self.object.opponent
            ).pokemons.all()
        context['user_is_opponent'] = True if self.object.opponent == self.request.user else False
        return context


class ChoosePokemonTeamView(LoginRequiredMixin, generic.FormView):
    template_name = 'battles/choose_team.html'
    form_class = ChooseTeamForm

    def get_initial(self):
        return {
            'trainer': self.request.user,
            'battle_related': Battle.objects.get(pk=self.kwargs['pk'])
            }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['battle'] = Battle.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('battles:details', kwargs={'pk': self.kwargs['pk']})
