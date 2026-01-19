from rest_framework.permissions import BasePermission


class IsAdvocateUser(BasePermission):
    """
    Allow only advocate users
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADVOCATE'
