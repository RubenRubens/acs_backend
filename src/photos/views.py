from django.contrib.auth.models import User
from django.http.response import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Subquery
from rest_framework.views import APIView
from django.http import FileResponse

from accounts.permissions import IsOwner, IsFollower
from accounts.models import Follow
from .models import Comment, Post
from .serializers import CommentSerializer, PostSerializer


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieve(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner | IsFollower]


class PostDestroy(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner]


class CommentCreate(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner | IsFollower]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieve(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner | IsFollower]


class CommentDestroy(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]


class PostList(APIView):
    '''
    List all posts of a given user
    '''
    permission_classes = [IsOwner | IsFollower]

    def get(self, request, user_pk):
        posts = Post.objects.filter(author__pk=user_pk).order_by('-date_published')
        if not posts:
            raise Http404
        self.check_object_permissions(request, User.objects.get(pk=user_pk))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CommentList(APIView):
    '''
    List all comments of a given post
    '''
    permission_classes = [IsOwner | IsFollower]

    def get(self, request, post_pk):
        comments = Comment.objects.filter(post__pk=post_pk).order_by('date_published')
        if not comments:
            raise Http404
        self.check_object_permissions(request, Post.objects.get(pk=post_pk))
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class RetrieveImage(APIView):
    '''
    Retrieve an image.
    '''
    permission_classes = [IsOwner | IsFollower]

    def get(self, request, post_pk):
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise Http404
        self.check_object_permissions(request, post)
        return FileResponse(open(post.image_file.path, 'rb'))


@api_view(['GET'])
def feed(request):
    following = Follow.objects.filter(follower=request.user).values('id')
    user_feed = Post.objects.annotate(author__pk=Subquery(following)).order_by('-date_published')
    serializer = PostSerializer(user_feed, many=True)
    return Response(serializer.data)
