from django.core.management.base import BaseCommand
from authentication.models import User, UserSettings
from authentication.serializers import UserSerializer
from yaml import serialize


class Command(BaseCommand):
    help = 'Seed initial categories into the database'

    def handle(self, *args, **kwargs):
        data = {
            "username": "admin",
            "password": "ChangeMe",
            "email": "admin@example.com",
            "is_superuser": True
        }

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            UserSettings.objects.create(user=instance)

            if instance:
                self.stdout.write(self.style.SUCCESS(f"Admin user created: {instance.email}"))
            else:
                self.stdout.write(f"Admin user already exists: {instance.email}")
        else:
            self.stdout.write(f"Serializer is not valid. {serializer.errors}")