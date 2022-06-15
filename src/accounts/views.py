from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.http.response import Http404
from django.http import FileResponse
from django.db import transaction
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .serializer import *
from .models import Account, FollowerPetition, Follow
from .permissions import *


class AccountList(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsOwner | ReadOnly]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_create(request):
    
    serializer = UserSerializer(data=request.data)
    serializer.is_valid()

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
        serializer = UserSerializer(user)

        # Return the user created
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(APIView):

    permission_classes = [IsOwner | IsFollower]
    
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        # Check permissions
        self.check_object_permissions(request, user)

        # Serialize and validate the data
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Update the user
        user.username = serializer.validated_data['username']
        user.first_name = serializer.validated_data['first_name']
        user.last_name = serializer.validated_data['last_name']
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Creates a new serializer for the user (contains the id)
        user = User.objects.get(username=serializer.validated_data['username'])
        serializer = UserSerializer(user)

        # Return the user updated
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class RetrieveLoggedUser(APIView):
    '''
    Retrieve the information of the logged in user
    '''
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class IAmAFollower(APIView):
    '''
    If you are a follower return a 200 code, otherwise return a 4xx.
    '''
    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        if request.user in Follow.following(user=user):
            return Response({'message': 'You are a follower of this user'})
        return Response(
            {'message': 'You are a not follower of this user'},
            status=status.HTTP_418_IM_A_TEAPOT
        )


class ListFollowers(APIView):
    '''
    List the followers of a certain user
    '''
    permission_classes = [IsOwner | IsFollower]

    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        self.check_object_permissions(request, user)
        queryset = Follow.followers(user)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class ListFollowing(APIView):
    '''
    List the users a certain user is following
    '''
    permission_classes = [IsOwner | IsFollower]

    def get(self, request, user_pk):
        user = get_object_or_404(User, pk=user_pk)
        self.check_object_permissions(request, user)
        queryset = Follow.following(user)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class RetrieveProfilePicture(APIView):
    '''
    Retrieve the profile picture
    '''

    def get(self, request, user_pk):
        account = get_object_or_404(Account, user__pk=user_pk)
        try:
            print("wtf")
            return FileResponse(open(account.profile_picture.path, 'rb'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


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


@api_view(['POST'])
def search_user(request):
    '''
    Search a user by username, first_name and last_name.
    '''
    serializer = SearchUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    name = serializer.validated_data['name']
    query_users = User.objects.filter(username__icontains=name)
    query_first_names = User.objects.filter(first_name__icontains=name)
    query_last_names = User.objects.filter(last_name__icontains=name)
    query = (query_users | query_first_names | query_last_names).distinct()
    serializer = UserSerializer(query, many=True)
    return Response(serializer.data)
