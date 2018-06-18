from rest_framework import permissions

from battles.models import Battle  # noqa


class IsInBattle(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return True
