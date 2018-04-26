from django.views import generic

from .models import Battle, BattleTeam


class EmailSimulationView(generic.TemplateView):
    template_name = 'templated_email/battle_result.email'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        battle = Battle.objects.filter(chosen_pokemons__isnull=False).first()
        context['username'] = battle.creator.get_short_name()
        context['relative_opponent'] = battle.opponent.get_short_name()
        context['winner'] = battle.winner.get_short_name()
        context['your_team'] = BattleTeam.objects.all().order_by(
            '-trainer').first().pokemons.all()
        context['opponent_team'] = BattleTeam.objects.all().order_by(
            'trainer').first().pokemons.all()
        return context
