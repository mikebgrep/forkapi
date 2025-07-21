from django.urls import path

from .views import CreateRestoreListBackup, RetrieveDeleteBackup, ImportBackup

app_name = "backupper"

urlpatterns = [
    path("", CreateRestoreListBackup.as_view()),
    path("<int:pk>/", RetrieveDeleteBackup.as_view()),
    path("import/", ImportBackup.as_view()),
]
