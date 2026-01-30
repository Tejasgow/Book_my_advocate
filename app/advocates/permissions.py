from rest_framework.permissions import BasePermission, SAFE_METHODS

# -----------------------------
# Only Advocates can access
# -----------------------------
class IsAdvocate(BasePermission):
    """
    Allows access only to users with role 'ADVOCATE'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'ADVOCATE')


# -----------------------------
# Admin users can write, others read-only
# -----------------------------
class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


# -----------------------------
# Only Assistant Lawyers (future use)
# -----------------------------
class IsAssistantLawyer(BasePermission):
    """
    Allows access only to users assigned as assistant lawyers.
    """
    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and hasattr(request.user, 'assistant_profile') 
            and request.user.assistant_profile.is_active
        )
