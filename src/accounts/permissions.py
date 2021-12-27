from rest_framework import permissions


class FollowerPermission(permissions.BasePermission):
    '''
    Check if the user is a follower of the author
    '''
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        try:
            Follow.objects.get(follower=request.user, user=obj.user)
            return True
        except:
            return False


class IsOwner(permissions.BasePermission):
    '''
    Permission to only allow the author of an object to edit it.
    '''
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUserOfTheAccount(permissions.BasePermission):
    '''
    Permission to only allow the author of an object to edit it.
    '''
    def has_object_permission(self, request, view, obj):
        return obj == request.user
