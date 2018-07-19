from rest_framework import serializers

from battles.models import Battle, BattleTeam
from pokemons.models import Pokemon
from pokemons.serializers import PokemonSerializer
from users.models import User


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
    status_label = serializers.ReadOnlyField()

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


class BattleListSerializer(BattleSerializer):
    is_creator = serializers.SerializerMethodField()

    def get_is_creator(self, obj):
        user = self.context['request'].user
        return obj.creator == user


class BattleCreationSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Battle
        fields = ('creator', 'opponent')

    def get_creator(self, obj):  # noqa
        user = self.context['request'].user
        return user.id

    def create(self, validated_data):
        # Get the request user, which is the battle creator
        validated_data['creator'] = User.objects.get(id=self.data['creator'])

        # Separate the pokemon
        pokemon_dict = self.context['request'].data['team']
        team = PokemonSerializer(data=pokemon_dict, many=True)
        team.is_valid()
        pokemon_ids = [pokemon['id'] for pokemon in team.data]
        pokemon = Pokemon.objects.filter(id__in=pokemon_ids)

        # Create the battle
        battle = Battle.objects.create(**validated_data)

        # Create the battle creator's team and reference the battle
        creator_team = BattleTeam.objects.create(trainer=battle.creator, battle_related=battle)
        creator_team.pokemons.add(*pokemon)

        return BattleSerializer(data=battle)
