import os

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from recipe.models import Recipe, Category
from recipe.utils import delete_file
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework import views

from forkapi.generics import RetrieveDestroyView, ListCreateUpdateView
from .models import BackupSnapshot
from .serializers import BackupSnapshotSerializer
from .utils import backup, unpack_and_apply_backup


class RetrieveDeleteBackup(RetrieveDestroyView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BackupSnapshot.objects.all()
    serializer_class = BackupSnapshotSerializer


class CreateRestoreListBackup(ListCreateUpdateView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BackupSnapshot.objects.all()
    serializer_class = BackupSnapshotSerializer
    pagination_class = None

    def post(self, request, *args, **kwargs):
        recipes = Recipe.objects.all()
        snapshot = backup(recipes)
        return Response(status=HTTP_201_CREATED, data={f"Successfully created backup file: {snapshot.file.name}"})

    def patch(self, request, *args, **kwargs):
        found_backup = get_object_or_404(BackupSnapshot, pk=request.data['backup_pk'])
        unpack_and_apply_backup(found_backup.file.name)
        return Response(status=HTTP_204_NO_CONTENT, data={f"Successfully loaded backup file: {found_backup.file.name}"})


class ImportBackup(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        upload_file = request.FILES['file']
        if not upload_file.name.endswith('.zip'):
            return Response(data={'errors': ["Only .zip files are allowed."]}, status=HTTP_400_BAD_REQUEST)

        destination = open('media/backups/' + upload_file.name, 'wb+')
        for chunk in upload_file.chunks():
            destination.write(chunk)
        destination.close()

        file_name = destination.name.replace("media/", "")

        snapshot, _ = BackupSnapshot.objects.get_or_create(file=file_name)
        snapshot.file.name = file_name
        snapshot.save()

        return Response(data=upload_file.name, status=HTTP_201_CREATED)
