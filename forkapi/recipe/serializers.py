from rest_framework import serializers

from .models import Category, Recipe, Ingredient, Step, Tag, LANGUAGES_CHOICES


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
    clear_video = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = Recipe
        fields = (
            "pk",
            "image",
            "name",
            "servings",
            "chef",
            "video",
            "description",
            "category",
            "tag",
            "prep_time",
            "cook_time",
            "total_time",
            "difficulty",
            "is_favorite",
            "ingredients",
            "steps",
            "clear_video",
            "reference",
        )

    def create(self, validated_data):
        """
        Make sure the image is present for create/post requests
        Remove clear_video from validated data on create
        """
        if 'image' not in validated_data:
            raise serializers.ValidationError({'image': 'Image is required for new recipes.'})

        if 'clear_video' in validated_data:
            validated_data.pop('clear_video')

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Set video to None if  on updated is removed clear_video write only bool should be set to True
        """
        if 'clear_video' in validated_data and validated_data['clear_video']:
            if instance.video:
                instance.video.delete()
            validated_data['video'] = None

        return super().update(instance, validated_data)


class RecipePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "pk",
            "image",
            "name",
            "chef",
            "servings",
            "total_time",
            "difficulty",
            "is_favorite",
        )


class RecipeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "pk",
            "image",
            "name",
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


class RecipeLinkSerializer(serializers.Serializer):
    url = serializers.URLField()

    class Meta:
        fields = (
            "url",
        )


class GenerateRecipeSerializer(serializers.Serializer):
    ingredients = serializers.ListField(child=serializers.CharField(), allow_empty=False)

    class Meta:
        fields = (
            "ingredients",
        )


class GenerateRecipeResultSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()
    thumbnail = serializers.URLField()

    class Meta:
        fields = (
            "name",
            "url",
            "thumbnail"
        )


class TranslateRecipeSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=LANGUAGES_CHOICES)
    recipe_id = serializers.IntegerField()

    class Meta:
        fields = (
            "language",
            "recipe_id"
        )