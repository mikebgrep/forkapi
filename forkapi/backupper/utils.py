import os
import zipfile
from datetime import datetime
from typing import List, Literal

from django.core.management import call_command
from recipe.utils import (
    get_files_from_folder_to_zip_paths,
    delete_file,
    move_file,
    delete_folder,
    delete_folder_files_only,
)

from .models import BackupSnapshot

base_temp_data_path = "backupper/data"
backup_json_database_file_path = f"{base_temp_data_path}/data.json"
media_images_folder = "media/images"
media_video_folder = "media/videos"
media_audio_folder = "media/audio"
media_backups_folder = "media/backups"


def backup():
    zip_file_name_with_path = os.path.join(
        media_backups_folder,
        f"fork_recipes_{datetime.now().date().strftime('%Y.%m.%d')}_{datetime.now().strftime('%H.%M.%S')}.zip",
    )

    snapshot = BackupSnapshot.objects.create()
    snapshot.file.name = zip_file_name_with_path.replace("media/", "")
    snapshot.save()

    backup_recipes(zip_file_name_with_path)

    return snapshot


def backup_recipes(zip_file_name_with_path: str):
    file_paths = []
    file_paths.extend(dump_database())
    file_paths.extend(dump_media())
    append_to_file(
        file_paths=file_paths, zip_file_name_with_path=zip_file_name_with_path, mode="w"
    )
    delete_file(backup_json_database_file_path)


def dump_database():
    with open(backup_json_database_file_path, "w", encoding="utf-8") as file:
        call_command("dumpdata", indent=4, format="json", stdout=file)

    return [(backup_json_database_file_path, "data.json/")]


def dump_media():
    file_paths = []
    file_paths.extend(get_files_from_folder_to_zip_paths(media_images_folder))
    file_paths.extend(get_files_from_folder_to_zip_paths(media_video_folder))
    file_paths.extend(get_files_from_folder_to_zip_paths(media_audio_folder))

    return file_paths


def append_to_file(
    file_paths: List, zip_file_name_with_path: str, mode: Literal["w", "a"]
):
    with zipfile.ZipFile(zip_file_name_with_path, mode) as myZipFile:
        for local_path, zip_path in file_paths:
            if local_path and os.path.exists(local_path):
                myZipFile.write(local_path, zip_path, zipfile.ZIP_DEFLATED)


def unpack_and_apply_backup(full_path: str):
    call_command("flush", interactive=False)
    from django.contrib.contenttypes.models import ContentType

    ContentType.objects.all().delete()
    upload_recipes(full_path)


def upload_recipes(full_path: str):
    zip_path = f"media/{full_path}"
    extract_to = os.path.join(
        base_temp_data_path, full_path.split("/")[-1].replace(".zip", "")
    )
    media_locations = [media_images_folder, media_audio_folder, media_video_folder]

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(extract_to)
        [delete_folder_files_only(x, ".md") for x in media_locations]

        for file in zip_file.namelist():
            if file.startswith("images/"):
                move_file(f"{extract_to}/{file}", media_images_folder)
            elif file.startswith("audio/"):
                move_file(f"{extract_to}/{file}", media_audio_folder)
            elif file.startswith("videos/"):
                move_file(f"{extract_to}/{file}", media_video_folder)

        if "data.json" in zip_file.namelist():
            call_command("loaddata", f"{extract_to}/data.json")
            delete_folder(extract_to)
