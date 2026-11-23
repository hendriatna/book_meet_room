from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.accounts.models import UserRole


class IsAdminOrReadOnly(BasePermission):
    """
    Authenticated users can read.
    Only ADMIN can create, update, and delete.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role == UserRole.ADMIN