from django import forms
from django.contrib import admin

from .models import *


class StepAdminForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
        }


class IngredientsInline(admin.TabularInline):
    model = Ingredient
    extra = 5


class StepsInline(admin.StackedInline):
    model = Step
    form = StepAdminForm
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Recipe Name", {"fields": ['name', 'difficulty']}),
        ("Recipe Group", {"fields": ['category', 'tag']}),
        ("Created date", {"fields": ['created_at']}),
        ("Reference", {"fields": ['chef', 'reference']}),
        ("Additional Info", {"fields": ['servings', 'prep_time', 'cook_time']}),
        ("Image", {"fields": ['image']}),
        ("Video", {"fields": ['video']}),

    ]
    list_display = ['name', 'category', 'tag']
    inlines = [IngredientsInline, StepsInline]
    search_fields = ['name', 'category__name', 'tag__name']
    list_filter = ['created_at']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)

