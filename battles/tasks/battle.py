from battles.helpers.battle import process_battle, run_battle
from battles.models import Battle
from pokebattle import celery_app


@celery_app.task
def process_battle_task(battle_id):
    # TODO: Check why battle.status isn't getting updated
    # import ipdb; ipdb.set_trace()
    battle = Battle.objects.get(id=battle_id)
    process_battle(battle)

    if battle.status == 'P':
        run_battle(battle)
