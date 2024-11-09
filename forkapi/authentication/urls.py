from django.urls import path

from .views import SignUpView, LoginView

app_name = "authentication"

urlpatterns = [
    path("signup", SignUpView.as_view()),
    path("token", LoginView.as_view()),
]