from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Django urls
    path('admin/', admin.site.urls),

    # Api urls
    path('api/v1/alunos/', include('apps.student.urls', namespace='student')),
    path('api/v1/user/', include('apps.abstract.urls', namespace='abstract')),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.abstract.views.view_404'
