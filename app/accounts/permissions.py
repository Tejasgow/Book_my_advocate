from rest_framework.permissions import BasePermission


# =================================================
# ADMIN PERMISSION
# =================================================

class IsAdmin(BasePermission):
    """
    Allows access only to users with ADMIN role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


# =================================================
# CLIENT PERMISSION
# =================================================

class IsClient(BasePermission):
    """
    Allows access only to users with CLIENT role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'CLIENT'
        )


# =================================================
# ADVOCATE PERMISSION
# =================================================

class IsAdvocate(BasePermission):
    """
    Allows access only to users with ADVOCATE role.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADVOCATE'
        )
