from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import Categories, TrendingRecipies, CategoryRecipes, FavoriteRecipes, Tags, TagsRecipies, SearchRecipies, \
    CreateCategory, UpdateCategory, RetrieveCreateDestroyRecipeSet, CreateIngredients, CreateSteps, UpdateRecipe, \
    CreateTag, \
    UpdateTag, ScrapeView, GenerateRecipeView, TranslateRecipeView, RetrieveRecipeLangVariationsView, \
    GenerateRecipeAudion

app_name = "recipe"

router_search = SimpleRouter()
router_search.register(r"home", SearchRecipies)
router_recipe = SimpleRouter()
router_recipe.register(r"", RetrieveCreateDestroyRecipeSet)

urlpatterns = [
    path("category", Categories.as_view()),
    path("trending", TrendingRecipies.as_view()),
    path("category/<int:pk>/recipes", CategoryRecipes.as_view()),
    path("tags", Tags.as_view()),
    path("tag/<int:pk>/recipes", TagsRecipies.as_view()),
    path("<int:pk>/favorite", FavoriteRecipes.as_view()),
    path('', include(router_search.urls)),
    path('', include(router_recipe.urls)),

    # Creation and update views
    path("category/add", CreateCategory.as_view()),
    path("category/<int:pk>", UpdateCategory.as_view()),
    path("tag/add", CreateTag.as_view()),
    path("tag/<int:pk>", UpdateTag.as_view()),
    path("<int:pk>", UpdateRecipe.as_view()),
    path("<int:pk>/ingredients", CreateIngredients.as_view()),
    path("<int:pk>/steps", CreateSteps.as_view()),
    path("scrape", ScrapeView.as_view()),
    path("generate", GenerateRecipeView.as_view()),
    path("translate", TranslateRecipeView.as_view()),
    path("<int:recipe_pk>/variations", RetrieveRecipeLangVariationsView.as_view()),
    path("audio", GenerateRecipeAudion.as_view()),
]
