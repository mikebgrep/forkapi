from rest_framework import serializers

from .models import Category, Recipe, Ingredient, Step, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
        )

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            "name",
            "quantity",
            "metric"
        )


class StepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = (
            "pk",
            "text"
        )


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True, read_only=True)
    steps = StepsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "pk",
            "image",
            "name",
            "serves",
            "video",
            "category",
            "tag",
            "prep_time",
            "is_favorite",
            "ingredients",
            "steps"
        )


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            "pk",
            "name",
        )

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()
        return instance