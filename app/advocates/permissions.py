from rest_framework.permissions import BasePermission, SAFE_METHODS


# =================================================
# Only Advocates
# =================================================
class IsAdvocate(BasePermission):
    """
    Allows access only to authenticated ADVOCATE users.
    Object-level access restricted to own profile.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_advocate()
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# =================================================
# Only Admin / Superuser
# =================================================
class IsAdmin(BasePermission):
    """
    Allows access only to admin or superuser users.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_admin() or user.is_staff or user.is_superuser)
        )


# =================================================
# Admin full access, others read-only
# =================================================
class IsAdminOrReadOnly(BasePermission):
    """
    Admin users have full access.
    Other users have read-only access.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_admin() or user.is_staff or user.is_superuser)
        )



# =================================================
# Assistant Lawyer
# =================================================
class IsAssistantLawyer(BasePermission):
    """
    Allows access only to active assistant lawyers.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        assistant = getattr(user, "assistant_profile", None)
        return bool(assistant and assistant.is_active)


# =================================================
# Advocate Profile Creation
# =================================================
class CanCreateAdvocateProfile(BasePermission):
    """
    Allows only ADVOCATE users to create their own profile.
    """

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.is_advocate()
        )
