from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static

from .views import docs_view

urlpatterns = [
    path('', TemplateView.as_view(template_name="config/landing_page.html")),
    path('account/', include('accounts.urls')),
    path('photos/', include('photos.urls')),
    path('docs/', docs_view.with_ui('redoc', cache_timeout=0))
]
