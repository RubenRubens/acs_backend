from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

docs_view = get_schema_view(
	openapi.Info(
		title='Paranoid Social Network API',
		default_version='dev',
		description='An opensource social network',
		license=openapi.License(name='MIT License')
	),
	public=True,
	permission_classes=[permissions.AllowAny]
)
