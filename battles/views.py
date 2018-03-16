from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import pokebase as pb

from pokemons.models import Pokemon

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
                pokemon_data = pb.pokemon(pokemon_id)
                stats = [(stats.stat.name, stats.base_stat) for stats in pokemon_data.stats]
            print('continue | ' + pokemon_id)
        return super().form_valid(form)