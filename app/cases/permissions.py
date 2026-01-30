from rest_framework.permissions import BasePermission

# -----------------------------
# Only Advocates Can Access Certain Views
# -----------------------------
class IsAdvocate(BasePermission):
    message = "Only advocates are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'advocate_profile')
        )


# -----------------------------
# Only Case Owner (Client) or Advocate Can Access
# -----------------------------
class IsCaseOwner(BasePermission):
    message = "You do not have access to this case."

    def has_object_permission(self, request, view, obj):
        # Client can access their own cases
        if obj.client == request.user:
            return True

        # Advocate can access their own cases
        if hasattr(request.user, 'advocate_profile'):
            return obj.advocate == request.user.advocate_profile

        return False
