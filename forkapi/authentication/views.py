from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer
from . import models
from forkapi.recipe.HeaderAuthentication import HeaderAuthentication


class SignUpView(generics.CreateAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


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


