from django.db import models
from recipe.models import BaseIngredient, Recipe



class ShoppingList(models.Model):
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    @property
    def recipes(self):
        return list({item.recipe.pk for item in self.items.all()})

class ShoppingItem(BaseIngredient):
    is_completed = models.BooleanField(default=False)
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name="items")
    times = models.IntegerField(default=1)



