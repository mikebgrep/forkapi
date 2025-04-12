import uuid
from datetime import datetime, timedelta
from enum import Enum

import django
from django.db import models
from django.db.models import Q
from .utils import calculate_recipe_total_time


def upload_to(instance, filename):
    return 'images/{uuid}_{filename}'.format(uuid=str(uuid.uuid4()), filename=filename)


def upload_video_to(instance, filename):
    return 'videos/{uuid}_{filename}'.format(uuid=str(uuid.uuid4()), filename=filename)


DIFFICULTY_CHOICES = [
    ('Easy', 'Easy'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
    ('Expert', 'Expert'),
]

LANGUAGES_CHOICES = [
    ('English', 'English'),
    ('Spanish', 'Español'),
    ('French', 'Français'),
    ('German', 'Deutsch'),
    ('Chinese', '中文'),
    ('Russian', 'Русский'),
    ('Italian', 'Italiano'),
    ('Japanese', '日本語'),
    ('Dutch', 'Nederlands'),
    ('Polish', 'Polski'),
    ('Greek', 'Ελληνικά'),
    ('Swedish', 'Svenska'),
    ('Czech', 'Čeština'),
    ('Bulgarian', 'Български'),
]


class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=170)
    servings = models.IntegerField()
    description = models.TextField(blank=False, null=False)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    video = models.FileField(upload_to=upload_video_to, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipies", blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="recipes", default=None, blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default=None, blank=True, null=True)
    chef = models.CharField(max_length=100, default=None, blank=True, null=True)
    reference = models.TextField(max_length=170, blank=True, null=True)
    language = models.CharField(max_length=20, choices=LANGUAGES_CHOICES, default='English')
    original_recipe_pk = models.IntegerField(default=None, blank=False, null=True)
    # prep_time & cook_time in minutes
    prep_time = models.IntegerField(default=0, null=True)
    cook_time = models.IntegerField(default=0, null=True)

    @property
    def is_trending(self):
        return self.created_at.date() >= (datetime.now() - timedelta(days=30)).date()

    @property
    def is_translated(self):
        return len(self.get_variations) > 1

    @property
    def is_original(self):
        return (self.is_translated and self.original_recipe_pk is None) or (
                not self.is_translated and self.original_recipe_pk is None)

    @property
    def get_variations(self):
        """
        Get variations of the recipes of any and the original recipe
        """
        recipes = Recipe.objects.filter(
            Q(original_recipe_pk=self.pk) | Q(pk=self.pk) if self.original_recipe_pk is None \
                else Q(original_recipe_pk=self.original_recipe_pk) | Q(pk=self.original_recipe_pk)
        )  ## Consider exclude self .exclude(pk=self.pk)

        return recipes

    # total_time calculated to hours
    @property
    def total_time(self) -> str | None:
        prep_time = int(self.prep_time.__repr__()) if self.prep_time is not None else 0
        cook_time = int(self.cook_time.__repr__()) if self.cook_time is not None else 0
        total = prep_time + cook_time

        if total == 0:
            return None

        return calculate_recipe_total_time(total)

    def __lt__(self, other):
        return self.pk > other.pk

    def __str__(self):
        return self.name


class BaseIngredient(models.Model):
    name = models.CharField(max_length=120)
    quantity = models.CharField(max_length=20)
    metric = models.CharField(max_length=11, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True


class Ingredient(BaseIngredient):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")

    def __str__(self):
        return self.name


class Step(models.Model):
    text = models.CharField(max_length=2000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")

    def __lt__(self, other):
        return self.pk > other.pk

    def get_step_number(self):
        step_pks = list(self.recipe.steps.values_list('pk', flat=True).order_by('pk'))
        return step_pks.index(self.pk) + 1 if self.pk in step_pks else None

    def __str__(self):
        index = self.get_step_number()
        return f"Step {index}" if index else f"Step (unsaved)"


class AudioInstructions(models.Model):
    file = models.FileField(blank=True, null=True)
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name="audio_instructions")

    def __str__(self):
        return f'{self.file}, {self.recipe.pk}'


class PromptType(Enum):
    MAIN_INFO = 0,
    INGREDIENTS = 1,
    INSTRUCTIONS = 2,
    GENERATE = 3,
