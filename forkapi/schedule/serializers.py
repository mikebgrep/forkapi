from rest_framework import serializers

from .models import Schedule
from recipe.models import Recipe


class ScheduleSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Schedule
        fields = (
            "pk",
            "timing",
            "date",
            "recipe",
            "recipe_id"
        )

