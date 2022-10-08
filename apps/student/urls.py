from django.urls import path
from apps.student.views import StudentApi, StudentEditApi

app_name = 'student'

urlpatterns = [
    path('', StudentApi.as_view()),
    path('<uuid:id>/', StudentEditApi.as_view()),
]
