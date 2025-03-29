import os

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_201_CREATED

from forkapi.authentication.HeaderAuthentication import HeaderAuthentication
from . import models, password_validation
from .models import PasswordResetToken, UserSettings
from .serializers import UserSerializer, ResetPasswordRequestSerializer, UserProfileSerializer, UserSettingsSerializer


class SignUpView(generics.CreateAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """
        Creating and UserSettings for the user
        """
        instance = serializer.save()
        UserSettings.objects.create(user=instance)


class LoginView(generics.CreateAPIView):
    """
    Retrieve Access Token for the user so can manage creating endpoint in recipe
    """
    authentication_classes = [HeaderAuthentication]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(models.User, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response("Forbidden", status.HTTP_403_FORBIDDEN)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        # Temporary workaround for default language for recipe.filters.FilterRecipeByLanguage
        os.environ["DEFAULT_RECIPE_DISPLAY_LANGUAGE"] = (user.settings.get().preferred_translate_language or "None")
        return Response({'token': token.key, 'user': serializer.data})


class UserProfileInfo(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DeleteAccountView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = models.User.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateUserPasswordUsernameAndEmail(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = models.User.objects.all()

    def put(self, request, *args, **kwargs):
        """
            Update password action
        """
        user = request.user
        new_password = request.data.get('new_password')
        old_password = request.data.get('old_password')

        if not user.check_password(old_password):
            return Response(data={"errors": ["Old password does not match current password"]},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            password_validation.validate_password_and_save_it(new_password, user=user)
        except ValidationError as ex:
            return Response(data={'errors': ex.messages}, status=HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        """
            Patch user username and email
        """
        partial = True
        instance = request.user
        serializer = UserSerializer(instance=instance, data=request.data, partial=partial)

        # TODO: Must be refactored errors from serializer -
        #  "{'username': [ErrorDetail(string='user with this username already exists.', code='unique')], 'email': [ErrorDetail(string='user with this email address already exists.', code='unique')]}"
        if not serializer.is_valid():
            errors = serializer.errors
            error_msg = "This email address already exists or is invalid.Please choice another."  if "email" in errors and \
                        "username" not in errors else "This username already exists.Please choice another." if "email" \
                        not in errors and "username" in errors else "This username and the email already exists.Please choice another."

            return Response(data={"errors": [error_msg]}, status=HTTP_409_CONFLICT)

        self.perform_update(serializer)
        return Response(serializer.data)


class RequestPasswordReset(generics.GenericAPIView):
    """
        View to handle creating of password reset token request
    """
    authentication_classes = [HeaderAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = request.data['email']
            user = models.User.objects.filter(email=email).first()

            if user:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                current_token = models.PasswordResetToken.objects.filter(email=email).first()
                password_reset_token = PasswordResetToken(email=email,
                                                          token=token) if not current_token else current_token
                password_reset_token.save()

                return Response(data={"token": password_reset_token.token}, status=status.HTTP_201_CREATED)

        return Response({"error": "User with provided email not found"}, status=status.HTTP_404_NOT_FOUND)


class ResetPassword(generics.GenericAPIView):
    """
        View to reset the password if their available reset token
        The token got deleted after usage
    """
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response(data={"errors": ["Confirm new password and the new password does not match"]},
                            status=HTTP_400_BAD_REQUEST)

        token_value = request.query_params.get("token")

        token = get_object_or_404(models.PasswordResetToken, token=token_value)
        if token:
            user = get_object_or_404(models.User, email=token.email)
            try:
                password_validation.validate_password_and_save_it(password, user=user)
            except ValidationError as ex:
                return Response(data={'errors': ex.messages}, status=HTTP_400_BAD_REQUEST)

            token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserSettingsView(generics.GenericAPIView):
    serializer_class = UserSettingsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        instance = UserSettings.objects.get(user=user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = request.user
        instance = UserSettings.objects.get(user=user)
        language = request.data.get('language')
        instance.preferred_translate_language = language
        instance.save()
        serializer = self.get_serializer(instance)
        # Temporary workaround for default language for recipe.filters.FilterRecipeByLanguage
        os.environ["DEFAULT_RECIPE_DISPLAY_LANGUAGE"] = language
        return Response(serializer.data, status=HTTP_201_CREATED)

