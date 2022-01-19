from django.contrib import admin
from django.urls import path, include

from .views import docs_view

urlpatterns = [
    path('account/', include('accounts.urls')),
    path('photos/', include('photos.urls')),
    path('docs/', docs_view.with_ui('redoc', cache_timeout=0))
]
