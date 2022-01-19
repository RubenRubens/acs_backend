from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('account/', include('accounts.urls')),
    path('photos/', include('photos.urls'))
]
