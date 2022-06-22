from rest_framework import permissions
from django.contrib.auth.models import User

from .models import Account, Follow, FollowerPetition


class IsOwner(permissions.BasePermission):
    '''
    Allow the author to do anything
    '''
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif isinstance(obj, User):
            return obj == request.user
        elif isinstance(obj, Account):
            return obj.user == request.user
        elif isinstance(obj, FollowerPetition):
            return obj.user == request.user
        return False


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


class IsFollowerReadOnly(permissions.BasePermission):
    '''
    Allow a follower to do anything
    '''
    def has_object_permission(self, request, view, obj):
        if not request.method in permissions.SAFE_METHODS:
            return False
        
        if hasattr(obj, 'author'):
            try:
                Follow.objects.get(follower=request.user, user=obj.author)
                return True
            except Follow.DoesNotExist:
                return False
        elif isinstance(obj, User):
            try:
                Follow.objects.get(follower=request.user, user=obj)
                return True
            except Follow.DoesNotExist:
                return False
        elif isinstance(obj, Account):
            try:
                Follow.objects.get(follower=request.user, user=obj.user)
                return True
            except Follow.DoesNotExist:
                return False


class ReadOnly(permissions.BasePermission):
    '''
    Limits the actions to be read only
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
