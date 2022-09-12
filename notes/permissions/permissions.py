from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """A permission class that will stop the super user from posting
    and editing any notes"""

    edit_methods = ("POST", "PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return False
        else:
            return True


class SharedPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("Allo", obj)
        return True
