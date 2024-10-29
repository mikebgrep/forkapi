from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
from .views import Categories, TrendingRecipies, CategoryRecipes, FavoriteRecipes, Tags, TagsRecipies, SearchRecipies

app_name = "recipe"

route = SimpleRouter()
route.register(r"favorites", FavoriteRecipes)

urlpatterns = [
    path("category", Categories.as_view()),
    path("trending", TrendingRecipies.as_view()),
    path("category/<int:pk>/recipes", CategoryRecipes.as_view()),
    path("tags", Tags.as_view()),
    path("tag/<int:pk>/recipes", TagsRecipies.as_view()),
    path("home", SearchRecipies.as_view()),
    path('', include(route.urls)),
]