from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
from .views import Categories, TrendingRecipies, CategoryRecipes, FavoriteRecipes, Tags, TagsRecipies, SearchRecipies, \
    CreateCategory, UpdateCategory

app_name = "foodie"

router = SimpleRouter()
router.register(r"home", SearchRecipies)

urlpatterns = [
    path("category", Categories.as_view()),
    path("trending", TrendingRecipies.as_view()),
    path("category/<int:pk>/recipes", CategoryRecipes.as_view()),
    path("tags", Tags.as_view()),
    path("tag/<int:pk>/recipes", TagsRecipies.as_view()),
    path("recipe/favorite", FavoriteRecipes.as_view()),
    path('', include(router.urls)),
    # Creation and update views
    path("category/add", CreateCategory.as_view()),
    path("category/<int:pk>", UpdateCategory.as_view())

]
