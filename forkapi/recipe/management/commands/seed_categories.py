from django.core.management.base import BaseCommand
from recipe.models import Category


class Command(BaseCommand):
    help = "Seed initial categories into the database"

    def handle(self, *args, **kwargs):
        categories = [
            "Greek 🌮",
            "Italian 🍝",
            "Mexican 🌶️",
        ]

        for name in categories:
            category, created = Category.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {name}"))
            else:
                self.stdout.write(f"Category already exists: {name}")
