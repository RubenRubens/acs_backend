from django.urls import path, include

from . import views

urlpatterns = [
    path('account/', views.AccountList.as_view()),
    path('account/<int:pk>/', views.AccountDetail.as_view()),
    path('profile_picture/<int:user_pk>/', views.RetrieveProfilePicture.as_view()),
    path('user/<int:pk>/', views.UserDetail.as_view()),
    path('registration/', views.user_create),
    path('petition/<int:pk>/', views.FollowerPetitionDetail.as_view()),
    path('petition/accept/', views.acept_follower_petition),
    path('petition/send/', views.send_follower_petition),
    path('petition/', views.list_follower_petitions),
    path('search/', views.search_user),
    path('followers/<int:user_pk>/', views.ListFollowers.as_view()),
    path('following/<int:user_pk>/', views.ListFollowing.as_view()),
    path('', include('dj_rest_auth.urls')),
]
