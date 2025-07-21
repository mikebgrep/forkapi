from django.db import models
from recipe.models import Recipe


class Schedule(models.Model):
    TIMING_CHOICES = [
        ("Breakfast", "Breakfast"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("Side", "Side"),
    ]

    timing = models.CharField(
        max_length=10, choices=TIMING_CHOICES, blank=False, null=False
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="schedule",
        blank=False,
        null=False,
    )
    date = models.DateField("yyyy-MM-dd")
