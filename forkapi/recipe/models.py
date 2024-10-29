from datetime import datetime, timedelta
import uuid
import django
from django.db import models
from django.db.models import BooleanField


def upload_to(instance, filename):
    return 'images/{uuid}_{filename}'.format(uuid=str(uuid.uuid4()) ,filename=filename)


def upload_vide_to(instance, filename):
    return 'videos/{uuid}_{filename}'.format(uuid=str(uuid.uuid4()), filename=filename)


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
    serves = models.IntegerField()
    is_favorite = BooleanField(default=False)
    created_at = models.DateTimeField(default=django.utils.timezone.now)
    image = models.ImageField(upload_to=upload_to, blank=False, null=False)
    video = models.FileField(upload_to=upload_vide_to, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="recipies", blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="recipes", default=None)
    prep_time = models.IntegerField(default=None, null=True)

    @property
    def is_trending(self):
        return self.created_at.date() >= (datetime.now() - timedelta(days=30)).date()

    def __lt__(self, other):
        return self.pk > other.pk

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=120)
    quantity = models.CharField(max_length=5)
    metric = models.CharField(max_length=10)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")


class Step(models.Model):
    text = models.CharField(max_length=2000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")

    def __lt__(self, other):
        return self.pk > other.pk
