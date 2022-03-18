from rest_framework import permissions

from .models import Follow


class IsOwner(permissions.BasePermission):
    '''
    Allow the author to do anything
    '''
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return obj == request.user


class IsFollower(permissions.BasePermission):
    '''
    Allow a follower to do anything
    '''
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            try:
                Follow.objects.get(follower=request.user, user=obj.author)
                return True
            except Follow.DoesNotExist:
                return False
        else:
            try:
                Follow.objects.get(follower=request.user, user=obj)
                return True
            except Follow.DoesNotExist:
                return False
