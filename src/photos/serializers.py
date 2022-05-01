from rest_framework import serializers
from django.urls import reverse

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
	image_url = serializers.SerializerMethodField()
	
	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ['date_published', 'author']
		extra_kwargs = {'image_file': {'write_only': True}}

	def get_image_url(self, post):
		return reverse('image', kwargs={'post_pk': post.pk})


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['date_published', 'author']
