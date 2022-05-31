from unittest import TestCase

from photos import likes_cache


class TestRedisStorage(TestCase):

	def test_storage(self):
		fake_pk = 202

		# Create a post
		likes_cache.create_post(fake_pk)
		self.assertEquals(likes_cache.get_likes(fake_pk), 0)

		# Add a like
		likes_cache.add_like(fake_pk)
		self.assertEquals(likes_cache.get_likes(fake_pk), 1)

		# Remove a like
		likes_cache.remove_like(fake_pk)
		self.assertEquals(likes_cache.get_likes(fake_pk), 0)

		# Destroy post
		likes_cache.destroy_post(fake_pk)
		self.assertEquals(likes_cache.get_likes(fake_pk), None)
