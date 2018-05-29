from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse


class UserIsPartOfBattleMixin(UserPassesTestMixin):
    permission_denied_message = 'You\'re not part of this battle!'
    redirect_field_name = None

    def test_func(self):
        battle = self.get_object()
        return self.request.user in [battle.creator, battle.opponent]

    def get_login_url(self):
        # default name of redirection method of AccessMixin, handle_no_permission() gives error
        messages.error(self.request, self.permission_denied_message)
        return reverse('battles:list')
