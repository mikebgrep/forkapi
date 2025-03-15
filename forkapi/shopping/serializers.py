from rest_framework import serializers
from .models import ShoppingItem, ShoppingList
from recipe.models import Ingredient, Recipe
from .utils import copy_object
from django.forms.models import model_to_dict

class ShoppingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingItem
        fields = (
            "pk",
            "name",
            "quantity",
            "metric",
            "times",
            "is_completed",

        )

class ShoppingItemPatchSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, required=False)
    quantity = serializers.CharField(max_length=20, required=False)
    metric = serializers.CharField(max_length=11,  required=False)
    is_completed = serializers.BooleanField(required=False)

    class Meta:
        model = ShoppingItem
        fields = (
            "name",
            "quantity",
            "metric",
            "is_completed",
        )


class ShoppingListSerializer(serializers.Serializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
        required=False
    )
    name = serializers.CharField(default=None)

    class Meta:
        fields = (
            "recipe",
            "name"
        )

    def create(self, validated_data):
        name = validated_data['name']
        shopping_list = ShoppingList.objects.create(name=name)

        return shopping_list

    def update(self, instance, validated_data):
        recipe = validated_data['recipe']
        found_recipe = Recipe.objects.get(pk=recipe.pk)

        # TODO: Find a better way to increment the times if the recipe is added second time to the list and the ingredients are same
        if found_recipe.pk in instance.recipes:
            for x in instance.items.all():
                if x.name in [z.name for z in found_recipe.ingredients.all()] and \
                    x.quantity in [z.quantity for z in found_recipe.ingredients.all()]:
                    x.times += 1
                    x.save()
        else:
            for x in found_recipe.ingredients.all():
                ingredient_data = model_to_dict(x, fields=['name', 'quantity', 'metric'])
                item = ShoppingItem(**ingredient_data)
                item.recipe = found_recipe
                item.shopping_list = instance
                item.save()

        return instance

    def to_representation(self, instance):
        return SingleShoppingListSerializer(context=self.context).to_representation(instance)


class SingleShoppingListSerializer(serializers.ModelSerializer):
    items = ShoppingItemSerializer(many=True)

    class Meta:
        model = ShoppingList
        fields = (
            "pk",
            "items",
            "name",
            "is_completed",
            "recipes",
        )
