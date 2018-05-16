from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse_lazy

from model_mommy import mommy

from battles.forms import CreateBattleForm
from battles.helpers.battle import run_battle
from battles.models import Battle, Invite
from battles.views import BattleView, CreateBattleView
from common.utils.tests import TestCaseUtils


class TestCreateBattleView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('battles:create-battle')
        self.user_opponent = mommy.make('users.User')
        self.battle = mommy.make('battles.Battle')
        self.view_class = CreateBattleView()
        self.battle_params = {
            'id': 2,
            'creator': self.user.id,
            'opponent': self.user_opponent.id
        }

    def test_response_status_200(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_create_battle_url_is_linked_to_view(self):
        self.assertEqual(
            resolve(self.view_url).func.__name__,
            CreateBattleView.as_view().__name__
        )

    def test_battle_creation(self):
        response = self.auth_client.post(self.view_url, self.battle_params)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, response.url)

    def test_if_redirects_non_logged(self):
        response = self.client.get(self.view_url)
        self.assertRedirects(
            response, expected_url='/login?next=/battles/create/')

    def test_battle_was_created_in_db(self):
        response = self.client.post(self.view_url, self.battle_params)
        battle = Battle.objects.filter(id=self.battle.id).exists()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(battle)

    def test_create_battle_view_form(self):
        self.assertEqual(self.view_class.get_form_class(), CreateBattleForm)

    def test_creating_a_battle_sends_invite_email(self):
        response = self.auth_client.post(self.view_url, self.battle_params)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], self.user_opponent.email)


class TestBattleDetailView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.pokemons = mommy.make('pokemons.Pokemon', _quantity=3)
        self.battle_team_creator = mommy.make('battles.BattleTeam',
                                              battle_related=self.battle,
                                              pokemons=self.pokemons,
                                              trainer=self.battle.creator)
        self.battle_team_opponent = mommy.make('battles.BattleTeam',
                                               battle_related=self.battle,
                                               pokemons=self.pokemons,
                                               trainer=self.battle.opponent)
        self.view_url = reverse_lazy('battles:details',
                                     kwargs={'pk': self.battle.id})

    def test_response_status_200(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_battle_details_url_is_linked_to_view(self):
        self.assertEqual(
            resolve(self.view_url).func.__name__,
            BattleView.as_view().__name__
        )

    def test_if_redirects_non_logged(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, expected_url='/login?next=/battles/details/{0}'.format(self.battle.id))


class TestChooseTeamView(TestCaseUtils, TestCase):

    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')
        self.view_url = reverse_lazy(
            'battles:team', kwargs={'pk': self.battle.id})
        self.battle_details_url = reverse_lazy(
            'battles:details', kwargs={'pk': self.battle.id}
        )
        self.battle_team_params = {
            'battle_related': self.battle,
            'first_pokemon': mommy.make('pokemons.Pokemon', id=1, hp=1, attack=1, defense=1).id,
            'second_pokemon': mommy.make('pokemons.Pokemon', id=2, hp=1, attack=1, defense=1).id,
            'third_pokemon': mommy.make('pokemons.Pokemon', id=3, hp=1, attack=1, defense=1).id
        }

    def test_pokemon_is_chosen(self):
        response = self.auth_client.post(self.view_url, self.battle_team_params)
        self.assertEqual(response.status_code, 302)

    def test_choosing_a_team_redirects_to_the_right_page(self):
        response = self.auth_client.post(self.view_url, self.battle_team_params)
        self.assertEqual(response.url, self.battle_details_url)

    def test_picking_just_one_team_doesnt_run_the_battle(self):
        response = self.auth_client.post(self.view_url, self.battle_team_params)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(run_battle(self.battle))

    def test_run_the_battle_when_it_has_two_teams(self):
        first_team_pokemons = mommy.make('pokemons.Pokemon', _quantity=3, attack=1, hp=1)
        mommy.make('battles.BattleTeam', battle_related=self.battle,
                   pokemons=first_team_pokemons, trainer=self.battle.creator)
        second_team_pokemons = mommy.make('pokemons.Pokemon', _quantity=3, attack=1, hp=1)
        mommy.make('battles.BattleTeam', battle_related=self.battle,
                   pokemons=second_team_pokemons, trainer=self.battle.opponent)
        self.auth_client.post(self.view_url)
        self.assertTrue(run_battle(self.battle))


class TestInviteView(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.view_url = reverse_lazy('battles:invite')

    def test_response_status_200(self):
        response = self.auth_client.post(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_non_logged_user(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/login?next=/battles/invite/')

    def test_invite_was_created_in_db(self):
        params = {
            'id': 1,
            'inviter': self.user,
            'invitee': 'example@user.com'
        }
        response = self.auth_client.post(self.view_url, params)
        invite = Invite.objects.filter(id=params['id']).exists()
        self.assertRedirects(response, expected_url=reverse_lazy('battles:invite'))
        self.assertTrue(invite)

    def test_inviting_user_shows_message(self):
        params = {
            'id': 1,
            'inviter': self.user,
            'invitee': 'example@user.com'
        }
        response = self.auth_client.post(self.view_url, params, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.extra_tags, 'user-invite')
