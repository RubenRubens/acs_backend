from django.db.models import fields
from rest_framework import serializers

from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
	# author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
	# author = serializers.CurrentUserDefault()
	class Meta:
		model = Post
		# fields = '__all__'
		fields = ['author', 'image_file']
		read_only_fields = ['date_published', 'author']
	
class CommentSerializer(serializers.ModelSerializer):
	author = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
	class Meta:
		model = Comment
		fields = '__all__'
		read_only_fields = ['date_published']
