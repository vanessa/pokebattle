from django.views import generic

from .forms import CreateBattleForm


class BattlesListView(generic.TemplateView):
    template_name = 'battles/battles_list.html'

class CreateBattleView(generic.FormView):
    template_name = 'battles/create_battle.html'
    form_class = CreateBattleForm
