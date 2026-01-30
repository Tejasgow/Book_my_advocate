from rest_framework.permissions import BasePermission


# =================================================
# ROLE-BASED PERMISSIONS
# =================================================

class IsAdvocateUser(BasePermission):
    """
    Allows access only to users with role 'ADVOCATE'.
    Useful for endpoints like approving/rejecting appointments
    or managing assistant lawyers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADVOCATE')


class IsClientUser(BasePermission):
    """
    Allows access only to users with role 'CLIENT'.
    Useful for endpoints like booking appointments.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'CLIENT')


# =================================================
# OBJECT-LEVEL PERMISSIONS
# =================================================

class IsOwnerOrAdvocate(BasePermission):
    """
    Object-level permission to allow access only to:
    - the client who owns the appointment
    - or the advocate assigned to the appointment
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and request.user.is_authenticated and
            (obj.user == request.user or obj.advocate.user == request.user)
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Allows full access to admin users, read-only for others.
    Useful for endpoints where only admins can verify advocates.
    """
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
