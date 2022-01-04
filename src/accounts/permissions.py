from rest_framework import permissions

from .models import Follow


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
        except Follow.DoesNotExist:
            return False


class IsOwner(permissions.BasePermission):
    '''
    Permission to only allow the author of an object to edit it.
    '''
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsUserOfTheAccount(permissions.BasePermission):
    '''
    Permission to only allow the author of an object to edit it.
    '''
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwnerOrReadOnlyIfIsFollower(permissions.BasePermission):
    '''
    Allows the author to do anything and allows a foller to retrieve the object.
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            try:
                Follow.objects.get(follower=request.user, user=obj.author)
                return True
            except Follow.DoesNotExist:
                pass
        return obj.author == request.user


class IsOwnerOrFollower_Post(permissions.BasePermission):
    '''
    Allows the author or any follower to do anything.
    '''
    def has_object_permission(self, request, view, obj):
        try:
            Follow.objects.get(follower=request.user, user=obj.author)
            return True
        except Follow.DoesNotExist:
            return obj.author == request.user

class IsOwnerOrFollower_User(permissions.BasePermission):
    '''
    Allows the author or any follower to do anything.
    '''
    def has_object_permission(self, request, view, obj):
        try:
            Follow.objects.get(follower=request.user, user=obj)
            return True
        except Follow.DoesNotExist:
            return obj == request.user
