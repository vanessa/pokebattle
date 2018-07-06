from rest_framework import serializers

from battles.models import Battle, BattleTeam
from pokemons.models import Pokemon
from users.serializers import UserSerializer


class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'


class BattleTeamSerializer(serializers.ModelSerializer):
    pokemons = PokemonSerializer(many=True)
    trainer = UserSerializer()

    class Meta:
        model = BattleTeam
        fields = ('pokemons', 'trainer')


class BattleSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()
    opponent = serializers.SerializerMethodField()
    winner = UserSerializer()
    status_label = serializers.ReadOnlyField()

    class Meta:
        model = Battle
        fields = '__all__'

    def get_creator(self, obj):
        qs = BattleTeam.objects.filter(battle_related=obj, trainer=obj.creator).first()
        # If user hasn't chosen a team,
        # only their username is needed
        user = UserSerializer(instance=obj.creator)
        if not qs:
            return {'trainer': user.data}
        serializer = BattleTeamSerializer(instance=qs)
        return serializer.data

    def get_opponent(self, obj):
        qs = BattleTeam.objects.filter(battle_related=obj, trainer=obj.opponent).first()
        user = UserSerializer(instance=obj.opponent)
        if not qs:
            return {'trainer': user.data}
        serializer = BattleTeamSerializer(instance=qs)
        return serializer.data


class BattleListSerializer(BattleSerializer):
    is_creator = serializers.SerializerMethodField()

    def get_is_creator(self, obj):
        user = self.context['request'].user
        return obj.creator == user
