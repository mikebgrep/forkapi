from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ExportDeleteBackup

app_name = "backupper"

urlpatterns = [
    path('', ExportDeleteBackup.as_view()),
]
