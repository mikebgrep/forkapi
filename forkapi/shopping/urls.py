from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

app_name = "shopping"

router_list = SimpleRouter()
router_list.register(r"", views.CreateListShoppingListView)

urlpatterns = [
    path('', include(router_list.urls)),
    path('complete-list/<int:pk>/', views.CompleteShoppingList.as_view()),
    path('item/<int:pk>/', views.ShoppingListItemView.as_view()),
    path('single/<int:pk>/', views.RetrieveUpdateShoppingListView.as_view())
]
