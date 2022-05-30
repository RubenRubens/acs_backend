from django.core.cache import cache
from config import settings

def likes_key(post_pk: int) -> str:
	'''
	They key used in the cache
	'''
	return f'{settings.LIKES}{post_pk}'

def create_post(post_pk: int):
	'''
	When a post is created the number of likes is set to 0
	'''
	cache.set(likes_key(post_pk), 0)

def destroy_post(post_pk: int):
	'''
	When a post is deleted the likes are removed as well 
	'''
	cache.delete(likes_key(post_pk))

def add_like(post_pk: int):
	'''
	Add one like to the post
	'''
	cache.incr(likes_key(post_pk))

def remove_like(post_pk: int):
	'''
	Subtract one like to the post
	'''
	cache.decr(likes_key(post_pk))

def get_likes(post_pk: int) -> int:
	'''
	Get the number of likes of a post
	'''
	return cache.get(likes_key(post_pk))
