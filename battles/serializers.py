from rest_framework import serializers

from battles.models import Battle, BattleTeam
from pokemons.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'


class BattleTeamSerializer(serializers.ModelSerializer):
    pokemons = PokemonSerializer(many=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = BattleTeam
        fields = ('pokemons', 'username')

    def get_username(self, obj):
        return obj.trainer.username


class BattleSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    opponent = serializers.SerializerMethodField()
    winner = serializers.SerializerMethodField()

    class Meta:
        model = Battle
        fields = '__all__'

    def get_creator(self, obj):
        qs = BattleTeam.objects.filter(battle_related=obj, trainer=obj.creator).first()
        # If user hasn't chosen a team,
        # only their username is needed
        if not qs:
            return {'username': obj.creator.get_short_name()}
        serializer = BattleTeamSerializer(instance=qs)
        return serializer.data

    def get_opponent(self, obj):
        qs = BattleTeam.objects.filter(battle_related=obj, trainer=obj.opponent).first()
        if not qs:
            return {'username': obj.opponent.get_short_name()}
        serializer = BattleTeamSerializer(instance=qs)
        return serializer.data

    def get_winner(self, obj):
        if not obj.winner:
            return None
        return obj.winner.get_short_name()
