import json
import os
import zipfile
from datetime import datetime
from typing import List, Literal

from recipe.models import Recipe, Category, AudioInstructions
from recipe.serializers import RecipesSerializer, CategorySerializer
from recipe.utils import delete_json_files_in_paths, instructions_and_steps_json_to_lists, save_recipe, \
    get_first_file_from_zip_file_folder

from .models import BackupSnapshot

base_path_backup = "media/backups"
base_temp_data_path = "backupper/data"
recipe_json_path = os.path.join(base_temp_data_path, "recipe_{0}.json")


def backup(recipes: List[Recipe]):
    zip_file_name_with_path = os.path.join(base_path_backup,
                                           f"fork_recipes_{datetime.now().date().strftime('%Y.%m.%d')}_{datetime.now().strftime('%H.%M.%S')}.zip")

    backup_recipes(recipes, zip_file_name_with_path)

    snapshot = BackupSnapshot.objects.create()
    snapshot.file.name = zip_file_name_with_path.replace("media/", "")
    snapshot.save()

    return snapshot


def backup_recipes(recipes: List[Recipe], zip_file_name_with_path: str):
    file_paths = []
    for index, recipe in enumerate(recipes):
        file_paths.extend(create_recipe_data_list(recipe, index))

    append_to_file(file_paths, zip_file_name_with_path, 'w')
    delete_json_files_in_paths(file_paths)


def append_to_file(file_paths: List, zip_file_name_with_path: str, mode: Literal['w', 'a']):
    with zipfile.ZipFile(zip_file_name_with_path, mode) as myZipFile:
        for local_path, zip_path in file_paths:
            if local_path and os.path.exists(local_path):
                myZipFile.write(local_path, zip_path, zipfile.ZIP_DEFLATED)


def create_recipe_data_list(recipe: Recipe, index: int):
    paths = []
    recipe_data = RecipesSerializer(recipe).data
    recipe_json_str = json.dumps(recipe_data, indent=4)
    root_path = "recipes"

    with open(recipe_json_path.format(index), 'w', encoding='utf8') as file:
        file.write(recipe_json_str)

    paths.append((recipe_json_path.format(index), f"{root_path}/{index}/recipe.json"))

    if recipe.image and hasattr(recipe.image, 'path'):
        image_path = recipe.image.path
        paths.append((image_path, f"{root_path}/{index}/image/{os.path.basename(image_path)}"))

    if recipe.video and hasattr(recipe.video, 'path'):
        video_path = recipe.video.path
        paths.append((video_path, f"{root_path}/{index}/video/{os.path.basename(video_path)}"))

    if hasattr(recipe, 'audio_instructions'):
        audio_path = recipe.audio_instructions.file.path
        paths.append((audio_path, f"{root_path}/{index}/audio/{os.path.basename(audio_path)}"))

    return paths


def unpack_and_apply_backup(full_path: str):
    Recipe.objects.all().delete()
    Category.objects.all().delete()
    upload_recipes(full_path)


def upload_recipes(full_path: str):
    processed_categories = []

    with zipfile.ZipFile(f"media/{full_path}", 'r') as zip_file:
        all_files = zip_file.namelist()
        recipe_folders = set(
            path.split('/')[1] for path in all_files
            if path.startswith('recipes/') and path.count('/') > 1
        )

        for folder in sorted(recipe_folders):
            base_path = f"recipes/{folder}/"
            image_folder = f"{base_path}image/"
            video_folder = f"{base_path}video/"
            audio_folder = f"{base_path}audio/"
            recipe_json_file_path = base_path + "recipe.json"

            if recipe_json_file_path in all_files:
                with zip_file.open(recipe_json_file_path) as recipe_json_file:
                    recipe_data = json.load(recipe_json_file)
                    category_data = recipe_data['category']
                    steps, ingredients = instructions_and_steps_json_to_lists(recipe_data['steps'],
                                                                              recipe_data['ingredients'])
                    recipe_data['image'] = get_first_file_from_zip_file_folder(zip_file, all_files, image_folder)
                    recipe_data['video'] = get_first_file_from_zip_file_folder(zip_file, all_files, video_folder)
                    del recipe_data['steps']
                    del recipe_data['ingredients']
                    del recipe_data['category']

                    if category_data:
                        if category_data['name'] not in [x.name for x in processed_categories]:
                            serializer = CategorySerializer(data=category_data)
                            if serializer.is_valid(raise_exception=True):
                                category = serializer.save()
                                processed_categories.append(category)

                    serializer = RecipesSerializer(data=recipe_data)
                    if serializer.is_valid(raise_exception=True):
                        recipe = serializer.save()
                        if category_data:
                            recipe.category = [x for x in processed_categories if x.name == category_data['name']][0]

                        audio_file = get_first_file_from_zip_file_folder(zip_file, all_files, audio_folder)
                        if audio_file:
                            AudioInstructions.objects.create(file=audio_file, recipe=recipe)
                        save_recipe(recipe, ingredients, steps)
