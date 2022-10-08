from django.urls import path

from apps.abstract.views import UserApi

app_name = 'abstract'

urlpatterns = [
    path('', UserApi.as_view()),
]
