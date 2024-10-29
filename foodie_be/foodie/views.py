from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import generics, filters, status
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .HeaderAuthentication import HeaderAuthentication
from .generics import UpdateAPIView, PatchAPIView, ListModelViewSet
from .models import Category, Recipe, Tag
from .serializers import RecipesSerializer, CategorySerializer, TagsSerializer, IngredientsSerializer, StepsSerializer


class SearchRecipies(ListModelViewSet):
    """
    View for fetching recipes ether from search keyword name or all favorites
    """
    authentication_classes = [HeaderAuthentication]
    pagination_class = PageNumberPagination
    serializer_class = RecipesSerializer

    queryset = Recipe.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=False)
    def favorites(self, request, *args, **kwargs):
        # Get all favorite recipes and sort them by pk
        favorite_recipes = get_list_or_404(Recipe, is_favorite=True).sort()
        serializer = self.get_serializer(favorite_recipes, many=True)
        return Response(serializer.data)


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

    def patch(self,  request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        if recipe.is_favorite:
            recipe.is_favorite = False
        else:
            recipe.is_favorite = True
        recipe.save()

        return Response(data=f"Success {"favorite" if recipe.is_favorite else "unfavorite"} recipe", status=HTTP_201_CREATED)

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
    authentication_classes = [HeaderAuthentication]
    serializer_class = CategorySerializer


class UpdateCategory(UpdateAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CreateTag(generics.CreateAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = TagsSerializer


class UpdateTag(UpdateAPIView):
    authentication_classes = [HeaderAuthentication]
    serializer_class = TagsSerializer
    queryset = Tag.objects.all()


class CreateRecipe(generics.CreateAPIView):
    """
    View for creating the recipe (only main info without ingredients and steps).
    """
    authentication_classes = [HeaderAuthentication]
    serializer_class = RecipesSerializer


class CreateIngredients(generics.CreateAPIView):
    """
    View for creating Ingredients (many) for recipe (recipe pk needs to be passwd in the response).
    """
    authentication_classes = [HeaderAuthentication]
    serializer_class = IngredientsSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = True
        return IngredientsSerializer(*args, **kwargs)

class CreateSteps(generics.CreateAPIView):
    """
    View for creating Steps (many) for recipe (recipe pk needs to be passwd in the response).
    """
    authentication_classes = [HeaderAuthentication]
    serializer_class = StepsSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['many'] = True
        return StepsSerializer(*args, **kwargs)

class UpdateRecipe(UpdateAPIView):
    """
    View for updating the recipe (only main info without ingredients and steps).
    """
    authentication_classes = [HeaderAuthentication]
    serializer_class = RecipesSerializer
    queryset = Recipe.objects.all()