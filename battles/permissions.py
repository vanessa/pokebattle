
from rest_framework import permissions


class IsInBattle(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user in [obj.creator, obj.opponent]
