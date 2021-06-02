from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            obj.author == request.user or
            request.user and request.user.is_authenticated and
            request.user.is_staff or
            request.user.is_superuser)
