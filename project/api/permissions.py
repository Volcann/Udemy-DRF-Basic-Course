from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""

        #allow only read and not change the object
        #SAFE_METHODS are methods that don't require or don't make any
        #changes to the object so a safe method would be for example HTTP GET
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id==request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to uptae their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_profile.id==request.user.id
