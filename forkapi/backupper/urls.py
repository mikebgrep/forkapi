from django.urls import path, include

from .views import CreateRestoreListBackup, DeleteBackup, ImportBackup

app_name = "backupper"

urlpatterns = [
    path('', CreateRestoreListBackup.as_view()),
    path('<int:pk>/', DeleteBackup.as_view()),
    path('import/', ImportBackup.as_view()),
]
