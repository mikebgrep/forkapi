import json
import os
import zipfile
from datetime import datetime
from typing import List, Literal

from recipe.models import Recipe, Category
from recipe.serializers import RecipesSerializer, CategorySerializer
from recipe.utils import delete_file

base_data_path = "backupper/data"
recipe_json_path = os.path.join(base_data_path, "recipe.json")
category_json_path = os.path.join(base_data_path, "category.json")
zip_file_name_with_path = os.path.join(base_data_path,
                                       f"fork_recipes_{datetime.now().date().strftime('%Y.%m.%d')}_{datetime.now().strftime('%H.%M.%S')}.zip")


def backup(recipes: List[Recipe], categories: List[Category]):
    backup_recipes(recipes)
    backup_categories(categories)

    return zip_file_name_with_path


def append_to_file(file_paths: List, mode: Literal['w', 'a']):
    with zipfile.ZipFile(zip_file_name_with_path, mode) as myZipFile:
        for local_path, zip_path in file_paths:
            if local_path and os.path.exists(local_path):
                myZipFile.write(local_path, zip_path, zipfile.ZIP_DEFLATED)


def backup_recipes(recipes: List[Recipe]):
    file_paths = []
    for index, recipe in enumerate(recipes):
        file_paths.extend(create_recipe_data_list(recipe, index))

    append_to_file(file_paths, 'w')
    delete_file(recipe_json_path)


def backup_categories(categories: List[Category]):
    file_paths = []
    for index, category in enumerate(categories):
        file_paths.extend(create_category_data_file(category, index))

    append_to_file(file_paths, 'a')
    delete_file(category_json_path)


def create_recipe_data_list(recipe: Recipe, index: int):
    paths = []
    recipe_data = RecipesSerializer(recipe).data
    recipe_json_str = json.dumps(recipe_data, indent=4)
    root_path = "recipes"

    with open(recipe_json_path, 'w', encoding='utf8') as file:
        file.write(recipe_json_str)

    paths.append((recipe_json_path, f"{root_path}/{index}/recipe.json"))

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


def create_category_data_file(category: Category, index: int):
    category_data = CategorySerializer(category).data
    category_json_str = json.dumps(category_data, indent=4)
    root_path = "categories"

    with open(category_json_path, 'w', encoding='utf8') as file:
        file.write(category_json_str)

    return [(category_json_path, f"{root_path}/{index}/category.json")]


def get_first_zip_file(directory=base_data_path):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.zip'):
            return filename, os.path.join(directory, filename)
    return None, None


def unpack_backup(full_path: str):


    with zipfile.ZipFile(full_path, 'r') as zip_file:
        # List all files in the ZIP to inspect its structure
        zip_file_contents = zip_file.namelist()

        print("Files in ZIP:", zip_file_contents)