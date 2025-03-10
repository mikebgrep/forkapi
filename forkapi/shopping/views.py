from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from forkapi import generics
from .models import ShoppingList, ShoppingItem
from .serializers import ShoppingListSerializer, ShoppingItemPatchSerializer


class CreateListShoppingListView(generics.ListCreateUpdateDestroyViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ShoppingListSerializer
    queryset = ShoppingList.objects.all()


class CompleteShoppingList(generics.PatchAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        shopping_list = get_object_or_404(ShoppingList, pk=kwargs['pk'])
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

        return Response(data=f"Success {"complete" if shopping_list.is_completed else "un-complete"} shopping list",
                        status=HTTP_201_CREATED)


class ShoppingListItemView(generics.UpdateDestroyView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemPatchSerializer



