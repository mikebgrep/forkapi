from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from forkapi.recipe.HeaderAuthentication import HeaderAuthentication
from . import models, password_validation
from .models import PasswordResetToken
from .serializers import UserSerializer, ResetPasswordRequestSerializer


class SignUpView(generics.CreateAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class LoginView(generics.CreateAPIView):
    """
    Retrieve Access Token for the user so can manage creating endpoint in recipe
    """
    authentication_classes = [HeaderAuthentication]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(models.User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response("Forbidden", status.HTTP_403_FORBIDDEN)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})


class DeleteAccountView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = models.User.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateUserPasswordUsernameAndEmail(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = models.User.objects.all()

    def put(self, request, *args, **kwargs):
        """
               Update password action
        """
        user = request.user
        new_password = request.data.get('new_password')
        old_password = request.data.get('old_password')

        if not user.check_password(old_password):
            return Response(data={"message": "Old password does not match current password"},
                            status=status.HTTP_400_BAD_REQUEST)

        return password_validation.validate_password_and_save_it(new_password, user=user)

    def patch(self, request, *args, **kwargs):
        """
            Patch user username and email
        """
        partial = True
        instance = request.user
        serializer = UserSerializer(instance=instance, data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)
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
            return Response(data={"message": "Confirm new password and the new password does not match"},
                            status=HTTP_400_BAD_REQUEST)

        token_value = request.query_params.get("token")

        token = get_object_or_404(models.PasswordResetToken, token=token_value)
        if token:
            user = get_object_or_404(models.User, email=token.email)
            token.delete()
            return password_validation.validate_password_and_save_it(password, user=user)
