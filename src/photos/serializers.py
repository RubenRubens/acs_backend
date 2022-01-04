from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = '__all__'
		read_only_fields = ['date_published', 'author']


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['date_published', 'author']
