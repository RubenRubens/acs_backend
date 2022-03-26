from typing import Tuple
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from ..models import Account, Follow, FollowerPetition


class AccountTest(TestCase):

    def setUp(self):

        # Data
        self.mario_data = {
            'username': 'mario',
            'password': 'secret_001',
            'first_name': 'Mario',
            'last_name': 'A.'
        }

        self.daniel_data = {
            'username': 'daniel',
            'password': 'secret_001',
            'first_name': 'Daniel',
            'last_name': 'B.'
        }
        
        self.vilma_data = {
            'username': 'unfriendly_user',
            'password': 'secret_001',
            'first_name': 'Vilma',
            'last_name': 'C.'
        }

        # Registration
        users, accounts = registration(self.daniel_data, self.mario_data, self.vilma_data)
        self.assertEquals(users, 3)
        self.assertEquals(accounts, 3)

        # Login
        tokens = login(self.daniel_data, self.mario_data, self.vilma_data)
        self.assertEquals(tokens, 3)

        # Set up test clients (Mario, Daniel and Vilman)
        self.mario_client, self.mario  = generateTestClient(self.mario_data['username'])
        self.daniel_client, self.daniel  = generateTestClient(self.daniel_data['username'])
        self.vilma_client, self.vilma  = generateTestClient(self.vilma_data['username'])

    def test_account_retrieve(self):
        '''
        Retrieves Mario's account
        '''
        response = self.mario_client.get(f'/account/account/{self.mario.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Follow(user=self.mario, follower=self.daniel).save()

        response = self.daniel_client.get(f'/account/account/{self.mario.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_retrieve_forbidden(self):
        '''
        A user tries to retrieve someone else account.
        '''
        response = self.vilma_client.get(f'/account/account/{self.daniel.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_retrieve(self):
        '''
        Retrieves Mario's user
        '''
        response = self.mario_client.get(f'/account/user/{self.mario.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        Follow(user=self.mario, follower=self.daniel).save()
        
        response = self.daniel_client.get(f'/account/user/{self.mario.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve_forbidden(self):
        '''
        A user tries to retrieve someone else user.
        '''
        response = self.vilma_client.get(f'/account/user/{self.daniel.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_delation(self):
        '''
        Deletes Mario's account
        '''
        self.mario_client.delete(f'/account/user/{self.mario.id}/')
        self.assertEqual(User.objects.filter(username=self.mario.username).count(), 0)
        self.assertEqual(Account.objects.filter(user__username=self.mario.username).count(), 0)

    def test_account_delation_forbidden(self):
        '''
        A user deletes someone else account.
        '''
        response = self.mario_client.delete(f'/account/user/{self.daniel.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.filter(username=self.daniel_data['username']).count(), 1)

    def test_petitions(self):
        # Send several petitions
        for _ in range(5):
            self.daniel_client.post(
                '/account/petition/send/',
                {'user': self.mario.id}
            )

        # There must be only one petition
        petitions = FollowerPetition.objects.all().count()
        self.assertEquals(petitions, 1)

        # Get the list of petitions
        request = self.mario_client.post('/account/petition/')
        self.assertEqual(len(request.data), 1)

        # Accept the petition
        self.mario_client.post(
            '/account/petition/accept/',
            {'possible_follower': self.daniel.id}
        )

        # There must be 0 follower petitions and 1 follower
        follower_petitions = FollowerPetition.objects.all().count()
        self.assertEqual(follower_petitions, 0)
        followers = Follow.objects.all().count()
        self.assertEqual(followers, 1)


def registration(*users_data) -> Tuple[int, int]:
    '''
    Creates new users and returns the number of users and accounts in the DB
    '''
    client = APIClient()
    for user_data in users_data:
        client.post('/account/registration/', user_data, format='json')

    users_number = User.objects.all().count()
    accounts_number = Account.objects.all().count()
    return users_number, accounts_number

def login(*users_data) -> int:
    '''
    Login users and returns the number of tokens in the DB
    '''
    client = APIClient()
    for user_data in users_data:
        client.post(
            '/account/login/',
            {'username': user_data['username'], 'password': user_data['password']}
        )

    token_number = Token.objects.all().count()
    return token_number

def generateTestClient(username: str) -> Tuple[APIClient, User]:
    '''
    Generates an authenticated APIClient ready to perform HTTP requests.
    Returns the generated client as well as the user
    '''
    token = Token.objects.get(user__username=username)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    user = User.objects.get(username=username)
    return client, user
