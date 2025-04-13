from django.db import models
import django


class BackupSnapshot(models.Model):
    file = models.FileField(upload_to='backups/', blank=False, null=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.file.name

    @property
    def size(self):
        return self.file.size
