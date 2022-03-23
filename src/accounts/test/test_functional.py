from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from ..models import Account, Follow, FollowerPetition


class AccountTest(TestCase):

    def setUp(self):
        '''
        Create two user accounts.
        '''
        client = APIClient()
        client.post(
            '/account/registration/',
            {
                'username': 'mario',
                'password': 'secret_001',
                'first_name': 'Mario',
                'last_name': 'A.'
            },
            format='json'
        )
        client.post(
            '/account/login/',
            {'username': 'mario', 'password': 'secret_001'}
        )

        client.post(
            '/account/registration/',
            {
                'username': 'daniel',
                'password': 'secret_001',
                'first_name': 'Daniel',
                'last_name': 'B.'
            },
            format='json'
        )
        client.post(
            '/account/login/',
            {'username': 'daniel', 'password': 'secret_001'}
        )

    def test_account_registration(self):
        users_number = User.objects.all().count()
        accounts_number = Account.objects.all().count()
        self.assertEquals(users_number, 2)
        self.assertEquals(accounts_number, 2)

    def test_user_tokens(self):
        '''
        Test login and logout.
        When a new user is created, no token is created.
        '''
        token_number = Token.objects.all().count()
        self.assertEquals(token_number, 2)

    def test_account_delation(self):
        # Set up the client
        client = APIClient()
        token = Token.objects.get(user__username='mario')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Obtain the user ID
        user_id = User.objects.get(username='mario').id

        # Delete the user
        client.delete(f'/account/user/{user_id}/')
        self.assertEqual(User.objects.filter(username='mario').count(), 0)

    def test_permission_account_delation(self):
        '''
        A user deletes someone else account.
        The user "not_lauren" tries to delete the account of "mario".
        '''
        # Set up the client (i.e. "daniel")
        client = APIClient()
        token = Token.objects.get(user__username='daniel')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Obtain mario's ID
        user_id = User.objects.get(username='mario').id

        # Delete the user mario
        response = client.delete(f'/account/user/{user_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.filter(username='mario').count(), 1)

    def test_send_follower_petition(self):
        # Set up the client
        client = APIClient()
        token = Token.objects.get(user__username='daniel')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Send a petition
        client.post(
            '/account/send_follower_petition/',
            {'user': User.objects.get(username='mario').id}
        )

        # There must be one follower petition
        queryset = FollowerPetition.objects.filter(
            user=User.objects.get(username='mario'),
            possible_follower=User.objects.get(username='daniel')
        )
        self.assertEquals(queryset.count(), 1)

    def test_accept_follower_petition(self):
        # Daniel sends a following petition to mario
        client_daniel = APIClient()
        token_daniel = Token.objects.get(user__username='daniel')
        client_daniel.credentials(HTTP_AUTHORIZATION='Token ' + token_daniel.key)
        client_daniel.post(
            '/account/send_follower_petition/',
            {'user': User.objects.get(username='mario').id}
        )

        # Mario accepts Daniel's petition
        client_mario = APIClient()
        token_mario = Token.objects.get(user__username='mario')
        client_mario.credentials(HTTP_AUTHORIZATION='Token ' + token_mario.key)
        client_mario.post(
            '/account/accept_follower_petition/',
            {'possible_follower': User.objects.get(username='daniel').id}
        )

        # There must be 0 follower petitions and 1 follower
        follower_petition_number = FollowerPetition.objects.all().count()
        self.assertEqual(follower_petition_number, 0)
        follow_number = Follow.objects.all().count()
        self.assertEqual(follow_number, 1)

    def test_follower_petition_list(self):
        # Daniel sends a following petition to Mario
        client_daniel = APIClient()
        token_daniel = Token.objects.get(user__username='daniel')
        client_daniel.credentials(HTTP_AUTHORIZATION='Token ' + token_daniel.key)
        client_daniel.post(
            '/account/send_follower_petition/',
            {'user': User.objects.get(username='mario').id}
        )

        # Mario get the list of petitions
        client_mario = APIClient()
        token_mario = Token.objects.get(user__username='mario')
        client_mario.credentials(HTTP_AUTHORIZATION='Token ' + token_mario.key)
        response = client_mario.get('/account/follower_petition_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
