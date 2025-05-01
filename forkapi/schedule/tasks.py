from datetime import timedelta
from django.utils import timezone
from .models import Schedule


def delete_old_schedules():
    cutoff_date = timezone.now() - timedelta(days=4)
    Schedule.objects.filter(date__lt=cutoff_date).delete()
