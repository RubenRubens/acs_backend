from django.urls import path

from . import views


urlpatterns = [
	path('post/', views.PostCreate.as_view()),
	path('post/<int:pk>/', views.PostDetail.as_view()),
	path('post_list/<int:user_pk>/', views.PostList.as_view()),
	path('image/<int:post_pk>/', views.RetrieveImage.as_view()),
	path('comment/', views.CommentCreate.as_view()),
	path('comment/<int:pk>/', views.CommentRetrieve.as_view()),
	path('comment_destroy/<int:pk>/', views.CommentDestroy.as_view()),
	path('comment_list/<int:post_pk>/', views.CommentList.as_view()),
]
