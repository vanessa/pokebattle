from rest_framework import permissions


class IsInBattle(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == (obj.creator or obj.opponent)
