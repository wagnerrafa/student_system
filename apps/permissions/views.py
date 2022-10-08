from rest_framework.permissions import BasePermission


class IsAuthenticatedOrWriteOnly(BasePermission):
    """
    The request is authenticated as a user, or is a write-only request.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated
