from django.urls import path
from apps.report_card.views import ReportCardApi, ReportCardEditApi

app_name = 'report_card'

urlpatterns = [
    path('', ReportCardApi.as_view()),
    path('<uuid:id>/', ReportCardEditApi.as_view()),
]
