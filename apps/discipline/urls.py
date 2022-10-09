from django.urls import path
from apps.discipline.views import DisciplineApi, DisciplineEditApi

app_name = 'discipline'

urlpatterns = [
    path('', DisciplineApi.as_view()),
    path('<uuid:id>/', DisciplineEditApi.as_view()),
]
