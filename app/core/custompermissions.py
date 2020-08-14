from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class PostPermission(permissions.BasePermission):
    """Allow user to edit their own posts"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own posts"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.postFrom.id == request.user.id
