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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            # Create new user
            user = User(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
            user.set_password(validated_data['password'])
            user.save()

            # Create new account
            account = Account(user=user)
            account.save()
            return user

    def update(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
