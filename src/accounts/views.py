from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth.models import User

from .serializer import (
    AccountSerializer,
    UserSerializer,
    FollowerPetitionSerializer,
    SendFollowerPetitionSerializer
)
from .models import Account, FollowerPetition, Follow
from .permissions import IsOwner


class AccountList(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]


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
