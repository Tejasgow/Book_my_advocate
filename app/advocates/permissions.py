from rest_framework.permissions import BasePermission

class IsAdvocate(BasePermission):
    """
    Allows access only to users with role 'ADVOCATE'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADVOCATE')
