from rest_framework import serializers
from django.urls import reverse
from django.core.cache import cache

from .models import Post, Comment
from .likes_cache import get_likes


class PostSerializer(serializers.ModelSerializer):
	image_url = serializers.SerializerMethodField(read_only=True)
	likes_number = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Post
		fields = ['author', 'image_file', 'date_published', 'likes_number', 'image_url']
		read_only_fields = ['date_published', 'author']
		extra_kwargs = {'image_file': {'write_only': True}}

	def get_image_url(self, post):
		return reverse('image', kwargs={'post_pk': post.pk})

	def get_likes_number(self, post):
		return get_likes(post.pk)


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['date_published', 'author']
