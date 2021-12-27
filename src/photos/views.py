from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes

from accounts.permissions import FollowerPermission
from .models import Comment, Post
from .serializer import CommentSerializer, PostSerializer

class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [FollowerPermission]
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [FollowerPermission]


class CommentList(generics.ListCreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	
	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

@api_view(['GET'])
@permission_classes([FollowerPermission])
def feed(request):
	queryset = Follow.objects.filter(user=)
	return Response()
