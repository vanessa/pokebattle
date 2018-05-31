from battles.models import Invite
from pokebattle import celery_app


@celery_app.task
def remove_used_invite(invite_id):
    invite = Invite.objects.get(id=invite_id)
    invite.delete()
