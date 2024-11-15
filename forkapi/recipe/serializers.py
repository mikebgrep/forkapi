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
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Ingredient
        fields = (
            "name",
            "quantity",
            "metric",
            "recipe_id"
        )


class StepsSerializer(serializers.ModelSerializer):
    recipe_id = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Step
        fields = (
            "text",
            "recipe_id"
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
            "servings",
            "video",
            "category",
            "tag",
            "prep_time",
            "cook_time",
            "total_time",
            "difficulty",
            "is_favorite",
            "ingredients",
            "steps"
        )


class RecipePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "pk",
            "image",
            "name",
            "servings",
            "total_time",
            "difficulty",
            "is_favorite",
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
