from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from model_mommy import mommy

from battles.helpers.emails import (
    send_battle_invite_email, send_inviter_email_when_invitee_chooses_team,
    send_pokebattle_invite_email
)


class TestBattleInviteEmail(TestCase):
    def setUp(self):
        super().setUp()
        self.battle = mommy.make('battles.Battle')

    def test_email_is_sent(self):
        send_battle_invite_email(self.battle)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_is_sent_with_correct_url(self):
        send_battle_invite_email(self.battle)
        correct_url = reverse('battles:details', args={self.battle.id})
        self.assertTrue(correct_url in mail.outbox[0].body)


class TestPokebattleInviteEmail(TestCase):
    def setUp(self):
        super().setUp()
        self.invite = mommy.make('battles.Invite', key=123)

    def test_email_is_sent(self):
        send_pokebattle_invite_email(self.invite)
        self.assertEqual(len(mail.outbox), 1)

    def test_email_sent_to_correct_recipient(self):
        send_pokebattle_invite_email(self.invite)
        recipient = mail.outbox[0].recipients()[0]
        self.assertEqual(recipient, self.invite.invitee)

    @override_settings(DOMAIN='https://pokebattle.com')
    def test_email_sent_with_correct_url(self):
        send_pokebattle_invite_email(self.invite)
        correct_url = 'https://pokebattle.com/login?key=123'
        mail_body = mail.outbox[0].body
        self.assertTrue(correct_url in mail_body)

    @override_settings(DOMAIN='https://pokebattle.com')
    def test_invitee_ready_to_battle_email(self):
        battle = mommy.make('battles.Battle')
        send_inviter_email_when_invitee_chooses_team(battle)

        mail_body = mail.outbox[0].body
        recipient = mail.outbox[0].to[0]
        correct_url = 'https://pokebattle.com/battles/details/1'

        self.assertTrue(correct_url in mail_body)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(recipient, battle.creator.email)
