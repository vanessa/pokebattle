import time

from battles.helpers.battle import run_battle
from battles.models import Battle
from pokebattle import celery_app


@celery_app.task
def run_battle_task(battle_id):
    time.sleep(5)
    battle = Battle.objects.get(id=battle_id)
    run_battle(battle)
