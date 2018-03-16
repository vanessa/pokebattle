from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

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
        return super().form_valid(form)