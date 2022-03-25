from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .serializer import *
from .models import Account, FollowerPetition, Follow
from .permissions import IsFollower, IsOwner


class AccountList(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_create(request):
    
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    with transaction.atomic():
        # Create a new user
        user = User(
            username=serializer.validated_data['username'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Create a new account
        account = Account(user=user)
        account.save()

        # Creates a new serializer for the user (contains the id)
        user = User.objects.get(username=serializer.validated_data['username'])
        serializer = CreateUserSerializer(user)

        # Return the user created
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):

    user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        # permissions = [IsOwner | IsFollower]
        # permissions.check_permissions(request.user, user)
        serializer = RetrieveUserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Check permissions
        # permissions = [IsOwner]
        # permissions.check_permissions(request.user, user)

        # Serialize and validate the data
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Update the user
        user.username = serializer.validated_data['username']
        user.first_name = serializer.validated_data['first_name']
        user.last_name = serializer.validated_data['last_name']
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Creates a new serializer for the user (contains the id)
        user = User.objects.get(username=serializer.validated_data['username'])
        serializer = UpdateUserSerializer(user)

        # Return the user updated
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        # permissions = [IsOwner]
        # permissions.check_permissions(request.user, user)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class FollowerPetitionDetail(RetrieveDestroyAPIView):
    queryset = FollowerPetition.objects.all()
    serializer_class = FollowerPetitionSerializer
    permission_classes = [IsOwner]


@api_view(['GET'])
def list_follower_petitions(request):
    '''
    List all the follower petitions that have this authenticated user.
    '''
    queryset = FollowerPetition.objects.filter(user=request.user)
    serializer = FollowerPetitionSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def send_follower_petition(request):
    '''
    Send a petition to follow another user.
    '''
    serializer = SendFollowerPetitionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        
        # Check if the petition has been already made
        try:
            follower_petition = FollowerPetition.objects.get(
                user=serializer.validated_data['user'],
                possible_follower=request.user
            )
            return Response(SendFollowerPetitionSerializer(follower_petition).data)

        # Create a new petition in case it has not been made before
        except FollowerPetition.DoesNotExist:
            follower_petition = FollowerPetition(
                user=serializer.validated_data['user'],
                possible_follower=request.user
            )
            follower_petition.save()
            return Response(SendFollowerPetitionSerializer(follower_petition).data)


@api_view(['POST'])
def acept_follower_petition(request):
    '''
    Acept the petition from an user. Expects the user ID of the new follower.
    '''
    serializer = FollowerPetitionSerializer(data=request.data)
    with transaction.atomic():
        try:
            if serializer.is_valid(raise_exception=True):
                accept_follower = serializer.validated_data['possible_follower']
                follower_petition = FollowerPetition.objects.get(
                    user=request.user,
                    possible_follower=accept_follower
                )
                follower_petition.delete()
                new_follower = Follow(
                    user=request.user,
                    follower=accept_follower
                )
                new_follower.save()
                return Response({'message': 'Follower accepted'})

        except FollowerPetition.DoesNotExist:
            return Response(
                {'Error': 'The petition does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
