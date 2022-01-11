from django.urls import path, include

from . import views

urlpatterns = [
    path('account/', views.AccountList.as_view()),
    path('account/<int:pk>/', views.AccountDetail.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('registration/', views.UserCreate.as_view()),
    path('follower_petition/<int:pk>/', views.FollowerPetitionDetail.as_view()),
    path('accept_follower_petition/', views.acept_follower_petition),
    path('send_follower_petition/', views.send_follower_petition),
    path('follower_petition_list/', views.list_follower_petitions),
    path('', include('dj_rest_auth.urls')),
]
