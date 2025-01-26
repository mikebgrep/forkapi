from rest_framework import serializers

from .models import Schedule
from recipe.models import Recipe
from recipe.serializers import RecipeScheduleSerializer


class ScheduleRepresentationSerializer(serializers.ModelSerializer):
    recipe = RecipeScheduleSerializer(read_only=True)

    class Meta:
        model = Schedule
        fields = (
            "pk",
            "timing",
            "date",
            "recipe",
        )


class ScheduleSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Schedule
        fields = (
            "pk",
            "timing",
            "date",
            "recipe",
        )

    def to_representation(self, instance):
        return ScheduleRepresentationSerializer(context=self.context).to_representation(instance)
