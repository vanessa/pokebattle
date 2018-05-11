from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.html import format_html
from django.views import generic

from dal import autocomplete

from battles.helpers.battle import run_battle
from battles.helpers.emails import send_battle_invite_email
from pokemons.models import Pokemon

from .forms import ChooseTeamForm, CreateBattleForm
from .models import Battle, BattleTeam


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
        return {'creator': self.request.user.id}

    def get_success_url(self):
        return reverse('battles:details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        send_battle_invite_email(self.object)
        return super().form_valid(form)


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
        context['user_is_opponent'] = self.object.opponent == self.request.user
        context['user_has_chosen_a_team'] = Pokemon.objects.filter(
            battle_team__battle_related=self.object,
            battle_team__trainer=self.request.user
        ).exists()
        return context


class PokemonListAPIView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return Pokemon.objects.none()

        qs = Pokemon.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

    def get_selected_result_label(self, item):
        return item.name

    def get_result_label(self, item):  # noqa
        return format_html('<img src="{}"> {}', item.sprite, item.name)


class ChoosePokemonTeamView(LoginRequiredMixin, generic.CreateView):
    template_name = 'battles/choose_team.html'
    form_class = ChooseTeamForm

    def get_success_url(self):
        return reverse('battles:details', kwargs={'pk': self.kwargs['pk']})

    def get(self, request, *args, **kwargs):
        battle_pk = kwargs['pk']
        battle_team = BattleTeam.objects.filter(
            battle_related__pk=battle_pk, trainer=request.user)
        if battle_team.exists():
            messages.error(request, 'You already chose a team!')
            return HttpResponseRedirect(reverse('battles:details', kwargs={'pk': battle_pk}))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        return {
            'trainer': self.request.user,
            'battle_related': Battle.objects.get(pk=self.kwargs['pk'])
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['battle'] = Battle.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        battle_team = form.save()
        run_battle(battle_team.battle_related)
        return HttpResponseRedirect(self.get_success_url())
