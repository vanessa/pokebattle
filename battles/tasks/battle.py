from battles.helpers.battle import process_battle, run_battle
from battles.models import Battle
from pokebattle import celery_app


@celery_app.task
def process_battle_task(battle_id):
    battle = Battle.objects.get(id=battle_id)
    process_battle(battle)


@celery_app.task
def run_battle_task(battle_id):
    battle = Battle.objects.get(id=battle_id)
    run_battle(battle)
