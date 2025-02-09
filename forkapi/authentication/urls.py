from django.urls import path

from . import views

app_name = "authentication"

urlpatterns = [
    path("signup", views.SignUpView.as_view()),
    path("token", views.LoginView.as_view()),
    path("delete-account", views.DeleteAccountView.as_view()),
    path("user", views.UpdateUserPasswordUsernameAndEmail.as_view()),
    path("user/info", views.UserProfileInfo.as_view()),
    path("password_reset", views.RequestPasswordReset.as_view()),
    path("password_reset/reset", views.ResetPassword.as_view()),
    path("settings", views.UserSettingsView.as_view())

]