from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/aluno/', include('apps.student.urls', namespace='student')),
    path('api/v1/disciplina/', include('apps.discipline.urls', namespace='discipline')),
    path('api/v1/boletim/', include('apps.report_card.urls', namespace='report_card')),
    path('api/v1/user/', include('apps.abstract.urls', namespace='abstract')),
    path('api/v1/docs/',
         TemplateView.as_view(template_name='api_documentation.html', extra_context={'schema_url': 'schema-api'}),
         name='api-docs'),
    path('api/v1/docs/deloitte/', get_schema_view(title="Project test Deloitte",
                                                  description="Api for a simple student and grade registration system",
                                                  version="1.0.0", permission_classes=[permissions.AllowAny]),
         name='schema-api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.abstract.views.view_404'
