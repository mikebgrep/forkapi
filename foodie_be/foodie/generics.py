from rest_framework import generics
from rest_framework import mixins

class UpdateAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Concrete view for updating a model instance.
    Only Put request
    """
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            generics.GenericAPIView):
    """
    Concrete view for retrieving, updating a model (patch only) instance.
    """
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)