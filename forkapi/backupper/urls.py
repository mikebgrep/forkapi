from django.urls import path, include

from .views import RetrieveDeleteBackup, CreateRestoreBackup, ListBackups

app_name = "backupper"

urlpatterns = [
    path('', CreateRestoreBackup.as_view()),
    path('<int:pk>/', RetrieveDeleteBackup.as_view()),
    path('all/', ListBackups.as_view()),
]
