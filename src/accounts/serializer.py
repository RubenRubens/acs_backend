from unicodedata import name
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Account, FollowerPetition, Follow

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['user']


class FollowerPetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerPetition
        fields = '__all__'
        read_only_fields = ['user', 'petition_time']


class SendFollowerPetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowerPetition
        fields = '__all__'
        read_only_fields = ['possible_follower', 'petition_time']


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['follow_time']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']
        extra_kwargs = {'password': {'write_only': True}}


class SearchUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
