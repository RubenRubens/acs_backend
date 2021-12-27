from django.urls import path

from . import views

urlpatterns = [
	path('post/', views.PostList.as_view()),
	path('post/<int:id>/', views.PostDetail.as_view()),
	path('comment/', views.CommentList.as_view()),
	path('comment/<int:id>/', views.CommentDetail.as_view()),
]
