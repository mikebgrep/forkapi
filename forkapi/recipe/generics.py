from rest_framework import mixins, generics, viewsets

class UpdateAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Concrete view for updating a model instance.
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PatchAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Concrete view for updating a model (patch only) instance.
    """
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ListModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Concrete view set for list a model instances.
    """
    def get(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)