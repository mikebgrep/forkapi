from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from urllib3 import request

from .HeaderAuthentication import HeaderAuthentication
from .generics import UpdateAPIView, PatchAPIView, ListModelViewSet, RetrieveCreateDestroyViewSet
from .models import Category, Recipe, Tag, Ingredient, Step
from .serializers import RecipesSerializer, CategorySerializer, TagsSerializer, IngredientsSerializer, StepsSerializer, \
    RecipePreviewSerializer


class SearchRecipies(ListModelViewSet):
    """
    View for fetching recipes ether from search keyword name or all favorites
    """
    authentication_classes = [HeaderAuthentication]
    pagination_class = PageNumberPagination
    serializer_class = RecipesSerializer

    queryset = Recipe.objects.all().order_by('created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=False)
    def favorites(self, request, *args, **kwargs):
        favorite_recipes = get_list_or_404(Recipe, is_favorite=True)
        favorite_recipes.sort()
        page = self.paginate_queryset(favorite_recipes)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, serializer_class=RecipePreviewSerializer)
    def preview(self, request, *args, **kwargs):
        preview_recipes = get_list_or_404(Recipe)
        preview_recipes.sort()
        page = self.paginate_queryset(preview_recipes)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class Categories(generics.ListAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = None


class CategoryRecipes(generics.ListAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = RecipesSerializer
    pagination_class = None

    def get_queryset(self):
        return Recipe.objects.select_related('category').filter(category_id=self.kwargs['pk'])


class TrendingRecipies(generics.ListAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = RecipesSerializer
    pagination_class = None

    def get_queryset(self):
        results_pks = [x.pk for x in Recipe.objects.all() if x.is_trending == True][:15]
        if len(results_pks) < 15:
            for pk in [x.pk for x in Recipe.objects.order_by('-pk')[:15 - len(results_pks)]]:
                results_pks.append(pk)

        return Recipe.objects.filter(pk__in=results_pks).order_by('-pk')


class FavoriteRecipes(PatchAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = RecipesSerializer
    queryset = Recipe.objects.all()

    def patch(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        if recipe.is_favorite:
            recipe.is_favorite = False
        else:
            recipe.is_favorite = True
        recipe.save()

        return Response(data=f"Success {"favorite" if recipe.is_favorite else "unfavorite"} recipe",
                        status=HTTP_201_CREATED)


class Tags(generics.ListAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class TagsRecipies(generics.ListAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = RecipesSerializer

    def get_queryset(self):
        recipies_pks = [x.pk for x in get_list_or_404(Recipe, tag__pk=self.kwargs['pk'])]
        return Recipe.objects.filter(pk__in=recipies_pks)


class CreateCategory(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer


class UpdateCategory(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CreateTag(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TagsSerializer


class UpdateTag(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()


class RetrieveCreateDestroyRecipeSet(RetrieveCreateDestroyViewSet):
    """
    View for creating a recipe (only main info without ingredients and steps)
    and delete (steps and ingredients inclusive)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecipesSerializer
    queryset = Recipe.objects.all()

    def get_authenticators(self):
        """
        Instantiates and returns the list of authentication_classes that this view requires.
        """
        if self.request.method == 'GET':
            authentication_classes = [HeaderAuthentication]
        else:
            authentication_classes = [TokenAuthentication]

        return [auth() for auth in authentication_classes]


class CreateIngredients(generics.CreateAPIView):
    """
    View for creating Ingredients (many) for recipe (recipe pk needs to be passwd in the response).
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientsSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = True
        return IngredientsSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('pk')

        # Perform delete of the current ingredients if any
        ingredients = Ingredient.objects.prefetch_related('recipe').filter(recipe_id=recipe_id)
        ingredients.delete()

        ingredients_data = serializer.validated_data
        for ingredient in ingredients_data:
            ingredient['recipe_id'] = recipe_id

        serializer.save()


class CreateSteps(generics.CreateAPIView):
    """
    View for creating Steps (many) for recipe (recipe pk needs to be passwd in the response).
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StepsSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = True
        return StepsSerializer(*args, **kwargs)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('pk')

        # Perform delete on current steps
        steps = Step.objects.prefetch_related('recipe').filter(recipe_id=recipe_id)
        steps.delete()

        steps_data = serializer.validated_data
        for step in steps_data:
            step['recipe_id'] = recipe_id

        serializer.save()


class UpdateRecipe(UpdateAPIView):
    """
    View for updating the recipe (only main info without ingredients and steps).
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RecipesSerializer
    queryset = Recipe.objects.all()
