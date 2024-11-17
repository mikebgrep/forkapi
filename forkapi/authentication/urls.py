from django.urls import path

from .views import SignUpView, LoginView, DeleteAccountView, UpdateUserPasswordUsernameAndEmail

app_name = "authentication"

urlpatterns = [
    path("signup", SignUpView.as_view()),
    path("token", LoginView.as_view()),
    path("delete-account", DeleteAccountView.as_view()),
    path('', UpdateUserPasswordUsernameAndEmail.as_view()),
]