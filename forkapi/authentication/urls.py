from django.urls import path

from .views import SignUpView

app_name = "authentication"

urlpatterns = [
    path("signup", SignUpView.as_view()),
]