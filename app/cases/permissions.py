from rest_framework.permissions import BasePermission


class IsAdvocate(BasePermission):
    message = "Only advocates are allowed."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'advocate_profile')
        )


class IsCaseOwner(BasePermission):
    message = "You do not have access to this case."

    def has_object_permission(self, request, view, obj):
        if obj.client == request.user:
            return True

        if hasattr(request.user, 'advocate_profile'):
            return obj.advocate == request.user.advocate_profile

        return False
