import pdb

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField(default=False)
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "is_superuser"
        )

    def create(self, validated_data):
        if self.validated_data.get("is_superuser"):
            return self.Meta.model.objects.create_superuser(**validated_data)
        return self.Meta.model.objects.create_user(**validated_data)

