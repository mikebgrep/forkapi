import os

from django.contrib.auth.models import AnonymousUser
from dotenv import load_dotenv
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


load_dotenv()


class HeaderAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            header = request.headers['X-Auth-Header']
            if header == os.getenv("X_AUTH_HEADER"):
                return AnonymousUser, header
            else:
                raise exceptions.AuthenticationFailed('Authentication header invalid')
        except KeyError:
            raise exceptions.AuthenticationFailed('You must use authentication header')
