from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from forkapi.recipe.HeaderAuthentication import HeaderAuthentication
from . import models, password_validation
from .serializers import UserSerializer


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

        return password_validation.validate_password(new_password, user=user)

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
