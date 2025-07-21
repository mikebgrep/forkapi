from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from forkapi import generics
from .models import ShoppingList, ShoppingItem
from .serializers import (
    ShoppingListSerializer,
    ShoppingItemPatchSerializer,
    SingleShoppingListSerializer,
    ShoppingItemSerializer,
)


class CreateListShoppingListView(generics.ListCreateUpdateDestroyViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ShoppingListSerializer
    queryset = ShoppingList.objects.all()


class RetrieveUpdateShoppingListView(generics.RetrieveUpdateView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SingleShoppingListSerializer
    queryset = ShoppingList.objects.all()

    def patch(self, request, *args, **kwargs):
        shopping_list = get_object_or_404(ShoppingList, pk=kwargs["pk"])
        data = request.data
        serializer = ShoppingItemSerializer(data=data)
        if serializer.is_valid():
            new_item = serializer.save(shopping_list=shopping_list)
            return Response(
                ShoppingItemSerializer(new_item).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteShoppingList(generics.PatchAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        shopping_list = get_object_or_404(ShoppingList, pk=kwargs["pk"])
        if shopping_list.is_completed:
            shopping_list.is_completed = False
            for x in shopping_list.items.all():
                x.is_completed = False
                x.save()
        else:
            shopping_list.is_completed = True
            for x in shopping_list.items.all():
                x.is_completed = True
                x.save()
        shopping_list.save()

        return Response(
            data=f"Success {'complete' if shopping_list.is_completed else 'incomplete'} shopping list",
            status=HTTP_201_CREATED,
        )


class ShoppingListItemView(generics.UpdateDestroyView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemPatchSerializer


class ShoppingListCompleteItemView(generics.PatchAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        item = get_object_or_404(ShoppingItem, pk=kwargs["pk"])

        if item.is_completed:
            item.is_completed = False
        else:
            item.is_completed = True

        item.save()

        # TODO:// may be implemented complete shopping list if all items are completed
        # if all(item.is_completed for item in item.shopping_list.items.all()):
        #     item.shopping_list.is_completed = True
        #     item.shopping_list.save()

        return Response(
            data=f"Success {'completed' if item.is_completed else 'incompleted'} item",
            status=HTTP_201_CREATED,
        )
