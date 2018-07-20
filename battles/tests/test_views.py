from django.core import mail
from django.test import RequestFactory
from django.urls import resolve, reverse

from model_mommy import mommy

from battles.forms import CreateBattleForm
from battles.helpers.battle import can_run_battle
from battles.models import Battle, BattleTeam, Invite
from battles.views import BattlesListView, BattleView, CreateBattleView
from common.utils.tests import TestCaseUtils


class TestCreateBattleView(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.view_url = reverse('battles:list')
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
            BattlesListView.as_view().__name__  # for React, the BattleListView is the main view
        )

    def test_if_redirects_non_logged(self):
        response = self.client.get(self.view_url, follow=True)
        redirection_url = response.request.get('PATH_INFO')
        next_page = response.context_data.get('next')
        self.assertResponse200(response)
        self.assertEqual(next_page, '/battles/')
        self.assertEqual(redirection_url, '/login/')

    def test_battle_was_created_in_db(self):
        response = self.client.post(self.view_url, self.battle_params)
        battle = Battle.objects.filter(id=self.battle.id).exists()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(battle)

    def test_create_battle_view_form(self):
        self.assertEqual(self.view_class.get_form_class(), CreateBattleForm)

    # TODO: Commented because it has to be transfered to create battle endpoint tests
    # def test_creating_a_battle_sends_invite_email(self):
    #     response = self.auth_client.post(self.view_url, self.battle_params)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertEqual(mail.outbox[0].to[0], self.user_opponent.email)


class TestBattleDetailView(TestCaseUtils):

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
        self.view_url = reverse('battles:details', kwargs={'pk': self.battle.id})

    def test_response_status_200(self):
        self.battle.creator = self.user
        self.battle.save()
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_battle_details_url_is_linked_to_view(self):
        self.assertEqual(
            resolve(self.view_url).func.__name__,
            BattleView.as_view().__name__
        )

    def test_redirects_non_logged(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url='/battles/', status_code=302,
                             target_status_code=302)

    def test_redirects_user_not_in_battle(self):
        response = self.client.get(self.view_url)
        self.assertResponse302(response)
        self.assertRedirects(response, expected_url='/battles/', status_code=302,
                             target_status_code=302)


class TestChooseTeamView(TestCaseUtils):

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.battle = mommy.make('battles.Battle', creator=self.user)
        self.view_url = reverse('battles:team', kwargs={'pk': self.battle.id})
        self.battle_team_params = {
            'battle_related': self.battle,
            'trainer': self.user,
            'first_pokemon': mommy.make('pokemons.Pokemon', id=1, hp=1, attack=1, defense=1).id,
            'second_pokemon': mommy.make('pokemons.Pokemon', id=2, hp=1, attack=1, defense=1).id,
            'third_pokemon': mommy.make('pokemons.Pokemon', id=3, hp=1, attack=1, defense=1).id
        }

    def test_pokemon_is_chosen(self):
        self.battle = mommy.make('battles.Battle', opponent=self.user)
        battle_team_params = {
            'battle_related': self.battle,
            'trainer': self.user,
            'first_pokemon': mommy.make('pokemons.Pokemon', id=1, hp=1, attack=1, defense=1).id,
            'second_pokemon': mommy.make('pokemons.Pokemon', id=2, hp=1, attack=1, defense=1).id,
            'third_pokemon': mommy.make('pokemons.Pokemon', id=3, hp=1, attack=1, defense=1).id
        }
        response = self.auth_client.post(self.view_url, battle_team_params)
        self.assertEqual(response.status_code, 302)

    def test_choosing_a_team_redirects_to_the_right_page(self):
        response = self.auth_client.post(self.view_url, self.battle_team_params)
        self.assertEqual(response.url, '/battles/')

    def test_run_the_battle_when_it_has_two_teams(self):
        first_team_pokemons = mommy.make('pokemons.Pokemon', _quantity=3, attack=1, hp=1)
        mommy.make('battles.BattleTeam', battle_related=self.battle,
                   pokemons=first_team_pokemons, trainer=self.battle.creator)
        second_team_pokemons = mommy.make('pokemons.Pokemon', _quantity=3, attack=1, hp=1)
        mommy.make('battles.BattleTeam', battle_related=self.battle,
                   pokemons=second_team_pokemons, trainer=self.battle.opponent)
        self.auth_client.post(self.view_url)
        self.assertTrue(can_run_battle(self.battle))

    def test_redirects_user_not_in_battle(self):
        self.battle = mommy.make('battles.Battle')
        self.view_url = reverse('battles:team', kwargs={'pk': self.battle.id})
        response = self.client.get(self.view_url)
        self.assertResponse302(response)

    def test_invitee_user_deletes_invite_when_choosing_for_the_first_time(self):
        inviter_user = mommy.make('users.User', email='inviter@email.com')
        mommy.make('battles.Invite', invitee=self.user.email, inviter=inviter_user)
        battle = mommy.make('battles.Battle', creator=inviter_user, opponent=self.user)
        view_url = reverse('battles:team', kwargs={'pk': battle.id})
        battle_team_data = {
            'battle_related': battle,
            'trainer': self.user,
            'first_pokemon': mommy.make('pokemons.Pokemon', id=1, hp=1, attack=1, defense=1).id,
            'second_pokemon': mommy.make('pokemons.Pokemon', id=2, hp=1, attack=1, defense=1).id,
            'third_pokemon': mommy.make('pokemons.Pokemon', id=3, hp=1, attack=1, defense=1).id
        }
        response = self.auth_client.post(view_url, battle_team_data)

        new_battle_team = BattleTeam.objects.last()

        self.assertResponse302(response)
        self.assertIsNotNone(new_battle_team)
        self.assertEqual(Invite.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 1)


class TestInviteView(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.view_url = reverse('invite')

    def test_response_status_200(self):
        response = self.auth_client.get(self.view_url)
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_non_logged_user(self):
        response = self.client.get(self.view_url, follow=True)
        redirection_url = response.request.get('PATH_INFO')
        next_page = response.context_data.get('next')
        self.assertResponse200(response)
        self.assertEqual(next_page, '/invite/')
        self.assertEqual(redirection_url, '/login/')

    def test_invite_was_created_in_db(self):
        params = {
            'id': 1,
            'inviter': self.user,
            'invitee': 'example@user.com'
        }
        response = self.auth_client.post(self.view_url, params)
        invite = Invite.objects.filter(id=params['id']).exists()
        self.assertRedirects(response, expected_url=self.view_url)
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

    def test_creating_invite_generates_key(self):
        params = {
            'id': 1,
            'inviter': self.user,
            'invitee': 'example@user.com'
        }
        response = self.auth_client.post(self.view_url, params, follow=True)
        invite = Invite.objects.get(id=params['id'])
        self.assertResponse200(response)
        self.assertTrue(invite.key is not None)
