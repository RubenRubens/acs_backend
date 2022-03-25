from django.db.models import fields
from django.db import transaction
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Account, FollowerPetition, Follow

class AccountSerializer(ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['user']


class FollowerPetitionSerializer(ModelSerializer):
    class Meta:
        model = FollowerPetition
        fields = '__all__'
        read_only_fields = ['user', 'petition_time']


class SendFollowerPetitionSerializer(ModelSerializer):
    class Meta:
        model = FollowerPetition
        fields = '__all__'
        read_only_fields = ['possible_follower', 'petition_time']


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['follow_time']


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}

class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']
        extra_kwargs = {'password': {'write_only': True}}


class RetrieveUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'first_name', 'last_name']
