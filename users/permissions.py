
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Checks if the authenticated user is the owner of the object """
    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.username
