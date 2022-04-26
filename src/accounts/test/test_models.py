from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Follow


class FollowModelTest(TestCase):

	def test_multiple_followers(self):
		N = 5
		influencer = User(username='mr_worldwide', password='demo')
		influencer.save()
		for num in range(N):
			user = User(username=f'user{num}', password='demo')
			user.save()
			follower = Follow(user=influencer, follower=user)
			follower.save()
		follower_number = Follow.objects.all().count()
		self.assertEqual(N, follower_number)

	def test_followers_query(self):
		N = 5

		influencer = User(username='mr_worldwide', password='demo')
		influencer.save()

		for num in range(N):
			user = User(username=f'user{num}', password='demo')
			user.save()
			follower = Follow(user=influencer, follower=user)
			follower.save()

		another_influencer = User(username='harris', password='demo')
		another_influencer.save()
		user = User(username=f'fakeuser', password='demo')
		user.save()
		follower = Follow(user=another_influencer, follower=user)
		follower.save()

		followers = Follow.followers(influencer)
		self.assertEqual(N, followers.count())

	def test_following_query(self):
		N = 5

		user = User(username='mr_worldwide', password='demo')
		user.save()

		for num in range(N):
			influencer = User(username=f'influencer{num}', password='demo')
			influencer.save()
			follower = Follow(user=influencer, follower=user)
			follower.save()

		following = Follow.following(user)
		self.assertEqual(N, following.count())
