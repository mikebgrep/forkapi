from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from forkapi.generics import RetrieveDestroyView
from recipe.models import Recipe, Category
from .utils import backup, get_first_zip_file
from recipe.utils import delete_file


class ExportDeleteBackup(RetrieveDestroyView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        existing_backup_file, full_path = get_first_zip_file()
        if existing_backup_file:
            return Response(status=HTTP_400_BAD_REQUEST, data={
                "errors": [f"Backup file already exists: {existing_backup_file}. Please delete it first!"]})

        recipes = Recipe.objects.all()
        categories = Category.objects.all()
        file_path = backup(recipes, categories)

        return FileResponse(open(file_path, 'rb'))

    def delete(self, request, *args, **kwargs):
        existing_backup_file, full_path = get_first_zip_file()
        if existing_backup_file:
            delete_file(full_path)
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(status=HTTP_400_BAD_REQUEST, data={
                "errors": [f"There no saved backup file."]})


class RestoreBackup():
    pass