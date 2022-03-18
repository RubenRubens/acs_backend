from django.contrib.auth.models import User
from django.http import response
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from .models import Post, Comment


class PostTest(TestCase):

    def setUp(self):
        '''
        Create two users. Daniel is a follower of Mario.
        '''
        client = APIClient()
        client.post(
            '/account/registration/',
            {
                'username': 'mario',
                'password': 'secret_001',
                'first_name': 'Mario',
                'last_name': 'A.'
            },
            format='json'
        )
        client.post(
            '/account/login/',
            {'username': 'mario', 'password': 'secret_001'}
        )

        client.post(
            '/account/registration/',
            {
                'username': 'daniel',
                'password': 'secret_001',
                'first_name': 'Daniel',
                'last_name': 'B.'
            },
            format='json'
        )
        client.post(
            '/account/login/',
            {'username': 'daniel', 'password': 'secret_001'}
        )

        # Set up the clients
        self.mario = APIClient()
        token_mario = Token.objects.get(user__username='mario')
        self.mario.credentials(HTTP_AUTHORIZATION='Token ' + token_mario.key)

        self.daniel = APIClient()
        token_daniel = Token.objects.get(user__username='daniel')
        self.daniel.credentials(HTTP_AUTHORIZATION='Token ' + token_daniel.key)

        # Daniel is following Mario
        self.daniel.post(
            '/account/send_follower_petition/',
            {'user': User.objects.get(username='mario').id}
        )

        self.mario.post(
            '/account/accept_follower_petition/',
            {'possible_follower': User.objects.get(username='daniel').id}
        )

    def test_create_post(self):
        '''
        Create new post.
        '''
        # Mario posts something
        self.mario.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )

        # Mario has successfully upload the picture
        self.assertEquals(Post.objects.filter(author__username='mario').count(), 1)
        self.assertEquals(Post.objects.get(author__username='mario').likes, 0)

    def test_list_posts(self):
        '''
        List all posts.
        '''
        POSTS_NUMBER = 4

        # Post some images
        for _ in range(POSTS_NUMBER):
            self.mario.post(
                '/photos/post/',
                {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
            )
        self.assertEquals(Post.objects.filter(author__username='mario').count(), POSTS_NUMBER)

        # Mario gets the list of all of the posts
        mario_user_id = User.objects.get(username="mario").id
        response = self.mario.get(f'/photos/post_list/{mario_user_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), POSTS_NUMBER)

        # Daniel gets the list of all of the posts
        response = self.daniel.get(f'/photos/post_list/{mario_user_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), POSTS_NUMBER)

    def test_destroy_post(self):
        '''
        Deletes a post.
        '''
        # Mario posts something
        self.mario.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )
        post_id = Post.objects.get(author__username='mario').id

        # Daniel attempts to delete the post
        self.daniel.delete(f'/photos/post_destroy/{post_id}/')
        self.assertEquals(Post.objects.filter(author__username='mario').count(), 1)

        # Mario deletes successfully the post
        self.mario.delete(f'/photos/post_destroy/{post_id}/')
        self.assertEquals(Post.objects.filter(author__username='mario').count(), 0)

    def test_retrieve_post(self):
        '''
        Retrieve a post.
        '''
        # Mario posts something
        self.mario.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )
        post_id = Post.objects.get(author__username='mario').id

        # Daniel attempts to retrieve the post
        response = self.daniel.get(f'/photos/post/{post_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Mario attemps to retrieve its own post
        response = self.mario.get(f'/photos/post/{post_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Daniel posts something
        self.daniel.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )
        post_id = Post.objects.get(author__username='daniel').id

        # Mario attempts to retrieve the post
        response = self.mario.get(f'/photos/post/{post_id}/')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_image(self):
        '''
        Retrieve an image from a post.
        '''
        # Mario posts something
        self.mario.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )
        post_id = Post.objects.get(author__username='mario').id

        # Daniel attempts to retrieve the image
        response = self.daniel.get(f'/photos/image/{post_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Mario attemps to retrieve its own image
        response = self.mario.get(f'/photos/image/{post_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Daniel posts something
        self.daniel.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )
        post_id = Post.objects.get(author__username='daniel').id

        # Mario attempts to retrieve the image
        response = self.mario.get(f'/photos/image/{post_id}/')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentTest(TestCase):

    def setUp(self):
        '''
        Create two users. Daniel is a follower of Mario.
        '''
        client = APIClient()
        client.post(
            '/account/registration/',
            {
                'username': 'mario',
                'password': 'secret_001',
                'first_name': 'Mario',
                'last_name': 'A.'
            },
            format='json'
        )
        client.post(
            '/account/login/',
            {'username': 'mario', 'password': 'secret_001'}
        )

        client.post(
            '/account/registration/',
            {
                'username': 'daniel',
                'password': 'secret_001',
                'first_name': 'Daniel',
                'last_name': 'B.'
            },
            format='json'
        )
        client.post(
            '/account/login/',
            {'username': 'daniel', 'password': 'secret_001'}
        )

        # Set up the clients
        self.mario = APIClient()
        token_mario = Token.objects.get(user__username='mario')
        self.mario.credentials(HTTP_AUTHORIZATION='Token ' + token_mario.key)
        
        self.daniel = APIClient()
        token_daniel = Token.objects.get(user__username='daniel')
        self.daniel.credentials(HTTP_AUTHORIZATION='Token ' + token_daniel.key)

        # Daniel is following Mario
        self.daniel.post(
            '/account/send_follower_petition/',
            {'user': User.objects.get(username='mario').id}
        )

        self.mario.post(
            '/account/accept_follower_petition/',
            {'possible_follower': User.objects.get(username='daniel').id}
        )

        # Mario creates a post
        self.mario.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )
        self.mario_post_id = Post.objects.get(author__username='mario').id

        # Daniel creates a post
        self.daniel.post(
            '/photos/post/',
            {'image_file': SimpleUploadedFile(name='test_image.jpg', content=open('photos/test/foo.jpg', 'rb').read(), content_type='image/jpeg')}
        )
        self.daniel_post_id = Post.objects.get(author__username='daniel').id

    def test_create_comment(self):
        '''
        Create a new comment.
        '''
        # Mario comment a post
        response = self.mario.post(
            '/photos/comment/',
            {'post': self.mario_post_id, 'text': 'Example comment'}
        )

        # Mario has successfully comment a post
        self.assertEquals(Comment.objects.filter(author__username='mario').count(), 1)

    def test_list_comments(self):
        '''
        List all comments of a particular post.
        '''
        COMMENTS_NUMBER = 4

        # Mario comments a post several times
        for _ in range(COMMENTS_NUMBER):
            self.mario.post(
                '/photos/comment/',
                {'post': self.mario_post_id, 'text': 'Example comment'}
            )
        self.assertEquals(Comment.objects.filter(post__pk=self.mario_post_id).count(), COMMENTS_NUMBER)

        # Mario gets the list of all of the comments
        response = self.mario.get(f'/photos/comment_list/{self.mario_post_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), COMMENTS_NUMBER)

        # Daniel gets the list of all of the comments
        response = self.daniel.get(f'/photos/comment_list/{self.mario_post_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), COMMENTS_NUMBER)

        # Daniel comment on Mario's post
        response = self.daniel.post(
            '/photos/comment/',
            {'post': self.mario_post_id, 'text': 'Example comment'}
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Comment.objects.filter(post__pk=self.mario_post_id).count(), COMMENTS_NUMBER + 1)

        # Mario gets the list of all of the comments again
        response = self.mario.get(f'/photos/comment_list/{self.mario_post_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), COMMENTS_NUMBER + 1)

        # Daniel comments on his own post
        for _ in range(COMMENTS_NUMBER):
            self.daniel.post(
                '/photos/comment/',
                {'post': self.daniel_post_id, 'text': 'Example comment'}
            )
        self.assertEquals(Comment.objects.filter(post__pk=self.daniel_post_id).count(), COMMENTS_NUMBER)

        # Mario gets the list of all Daniel's comments
        response = self.mario.get(f'/photos/comment_list/{self.daniel_post_id}/')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_comment(self):
        '''
        Deletes a comment.
        '''
        # Mario comments in it's own post
        self.mario.post(
            '/photos/comment/',
            {'post': self.mario_post_id, 'text': 'demo comment'}
        )
        comment_id = Comment.objects.get(post__pk=self.mario_post_id).id

        # Daniel attempts to delete Mario's comment
        response = self.daniel.delete(f'/photos/comment_destroy/{comment_id}/')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEquals(Comment.objects.filter(post__pk=self.mario_post_id).count(), 1)

        # Mario deletes successfully the comment
        response = self.mario.delete(f'/photos/comment_destroy/{comment_id}/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Comment.objects.filter(post__pk=self.mario_post_id).count(), 0)

    def test_retrieve_comment(self):
        '''
        Retrieve a comment.
        '''
        # Mario comments something
        self.mario.post(
            '/photos/comment/',
            {'post': self.mario_post_id, 'text': 'some random comment'}
        )
        comment_id = Comment.objects.get(post__id=self.mario_post_id).id

        # Daniel attempts to retrieve the comment
        response = self.daniel.get(f'/photos/comment/{comment_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Mario attemps to retrieve its own comment
        response = self.mario.get(f'/photos/comment/{comment_id}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Daniel comments something on his own post
        self.daniel.post(
            '/photos/comment/',
            {'post': self.daniel_post_id, 'text': 'some random comment'}
        )
        comment_id = Comment.objects.get(post__id=self.daniel_post_id).id

        # Mario attempts to retrieve Daniel's comment
        response = self.mario.get(f'/photos/comment/{comment_id}/')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
