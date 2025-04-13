from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from recipe.models import Recipe, Category
from recipe.utils import delete_file
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from forkapi.generics import RetrieveDestroyView, RetrieveCreateView, ListView
from .models import BackupSnapshot
from .serializers import BackupSnapshotSerializer
from .utils import backup, unpack_and_apply_backup


class RetrieveDeleteBackup(RetrieveDestroyView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BackupSnapshotSerializer
    queryset = BackupSnapshot.objects.all()


class CreateRestoreBackup(RetrieveCreateView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.all()
        snapshot = backup(recipes)
        return Response(status=HTTP_201_CREATED, data={f"Successfully created backup file: {snapshot.file.name}"})

    def post(self, request, *args, **kwargs):
        found_backup = get_object_or_404(BackupSnapshot, pk=request.data['backup_pk'])
        unpack_and_apply_backup(found_backup.file.name)
        return Response(status=HTTP_204_NO_CONTENT, data={f"Successfully loaded backup file: {found_backup.file.name}"})


class ListBackups(ListView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BackupSnapshotSerializer
    queryset = BackupSnapshot.objects.all()
    pagination_class = None
