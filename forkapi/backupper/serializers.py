from rest_framework import serializers

from .models import BackupSnapshot


class BackupSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackupSnapshot
        fields = (
            "pk",
            "file",
            "created_at",
            "size",
        )
