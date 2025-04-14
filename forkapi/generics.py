from rest_framework import mixins, generics, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


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


class RetrieveCreateDestroyViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    """
    Concrete view for get by id, deleting and creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListCreateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """
    Concrete view for list a model, deleting and creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListCreateUpdateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin,
                                     viewsets.GenericViewSet):
    """
    Concrete view for list, create, update, partial update and destroy a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UpdateDestroyView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Concrete view for patch and delete model instance
    """

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Concrete view to retrieve and update model instance
    """

    def get(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DestroyView(mixins.DestroyModelMixin, generics.GenericAPIView):
    """
    Concrete view to delete a model instance
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ListCreateUpdateView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Concrete view to retrieve and create a model instance
    """

    def get(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
