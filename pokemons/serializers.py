from rest_framework import serializers

from pokemons.models import Pokemon


class PokemonSerializer(serializers.ModelSerializer):
    label = serializers.ReadOnlyField(source='name')
    value = serializers.ReadOnlyField(source='id')

    class Meta:
        model = Pokemon
        fields = ('label', 'value', 'sprite', 'attack', 'defense', 'hp', )
