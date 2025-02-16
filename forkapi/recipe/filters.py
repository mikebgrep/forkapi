import os

from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv

from .models import Recipe


load_dotenv()

class FilterRecipeByLanguage(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        translated_language = os.getenv("DEFAULT_RECIPE_DISPLAY_LANGUAGE")
        if translated_language:
            translated_recipes = [x for x in queryset if x.language == translated_language]

            # TODO:// If the majority of recipes are not in english this will not take effect to hide the default language used in the app without to be set anywhere
            exclude_recipes = [x for x in queryset if x.is_translated and x.language != translated_language and x.language != "English"]

            non_translated_recipes = [x for x in queryset if x not in translated_recipes and \
                                      len([y for y in translated_recipes if y.original_recipe_pk == x.pk]) < 1 and x not in exclude_recipes]

            non_translated_recipes += translated_recipes
            return Recipe.objects.filter(pk__in=[x.pk for x in non_translated_recipes])

        return super().filter_queryset(request, queryset, view)
