from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views import generic

from pokemons.models import Pokemon

from .forms import ChooseTeamForm, CreateBattleForm
from .models import Battle


class BattlesListView(LoginRequiredMixin, generic.ListView):
    template_name = 'battles/battles_list.html'
    context_object_name = 'battles_created'
    
    def get_queryset(self):
        return Battle.objects.filter(creator=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['battles_invited'] = Battle.objects.filter(
            opponent=self.request.user
        )
        return context

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
        context['creators_pokemons'] = Pokemon.objects.filter(
            battle_team__battle_related=self.object,
            battle_team__trainer=self.object.creator
        )
        context['opponents_pokemons'] = Pokemon.objects.filter(
            battle_team__battle_related=self.object,
            battle_team__trainer=self.object.opponent
        )
        context['user_is_opponent'] = True if self.object.opponent == self.request.user else False
        context['user_has_chosen_a_team'] = Pokemon.objects.filter(
            battle_team__battle_related=self.object,
            battle_team__trainer=self.request.user
        ).exists()
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
