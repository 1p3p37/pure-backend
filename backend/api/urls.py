from django.conf import settings
from django.urls import include, path

from .views import HealthcheckAPIView


urlpatterns = [
    path('healthcheck/', HealthcheckAPIView.as_view(), name='healthcheck'),
]


if settings.BACKEND_SETTINGS_MODE != 'production':
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        # DRF_SPECTACULAR
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'swagger/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui',
        ),
    ]
