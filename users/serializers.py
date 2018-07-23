from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    value = serializers.ReadOnlyField(source='id')
    label = serializers.ReadOnlyField(source='username')

    class Meta:
        model = User
        fields = ('value', 'label', )
