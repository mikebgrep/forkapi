import json
import os
from pathlib import Path
from typing import List, Union
from urllib.parse import unquote

import requests
from django.core.files.base import ContentFile

from .models import Recipe, Ingredient, Step


def download_media_files(address: str, recipe_name: str, is_video: bool):
    recipe_name = recipe_name.replace("/", "")
    file_path = os.getcwd() + os.sep + "media" + os.sep + "temp_recipe_media" + os.sep + f"{recipe_name}.png" if not is_video else f"{recipe_name}.mp4"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    response = requests.get(address if 'https://' in address else f'https://{address}', stream=True, headers=headers)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(response.content)
            del response

    return file_path


def delete_file(file_path: str):
    os.remove(file_path)


def get_first_matching_link(words: str, strings: List[str]) -> str | None:
    """
        Used to get the first link that contains all the matching recipe words
    """
    for string in strings:
        if all(word.lower() in string for word in words):
            return string
        elif len([word.lower() in string for word in words]) >= 2:
            return string

    return None


def remove_stop_words(text: str):
    stop_words = {
        "a", "an", "the", "and", "or", "but", "if", "then", "of", "on",
        "in", "to", "with", "at", "by", "from", "for", "about", "as",
        "into", "like", "through", "over", "between", "out", "against",
        "during", "without", "within", "along", "around", "before",
        "after", "above", "below", "up", "down", "under", "again",
        "further", "once"
    }
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]

    return filtered_words


def parse_recipe_info(json_response: str):
    json_response = json_response.replace("```", "").replace("json", "")
    json_content = json.loads(json_response)
    return json_content


def manage_media(json_content_main_info, is_video: bool):
    image_url = json_content_main_info['image'] if not is_video else json_content_main_info['video']
    file_path = download_media_files(address=image_url, recipe_name=json_content_main_info['name'], is_video=is_video)
    if not is_video:
        del json_content_main_info['image']
    else:
        del json_content_main_info['video']
    return file_path


def extract_link_from_duckduck_go_url_result(url: str) -> str:
    print(url)
    try:
        link_with_ext = url.split("?uddg=")[1]
    except IndexError as ex:
        print(ex)
        link_with_ext = url

    encoded_url = link_with_ext.split("&rut")[0]

    return unquote(encoded_url)


def instructions_and_steps_json_to_lists(json_content_steps: dict, json_content_ingredients: dict):
    from .models import Ingredient, Step
    steps = []
    ingredients = []

    for instruction in json_content_steps:
        step = Step(**instruction)
        steps.append(step)

    for ingredient in json_content_ingredients:
        ingredient = Ingredient(**ingredient)
        ingredients.append(ingredient)

    return steps, ingredients


def save_recipe(recipe: Recipe, ingredients: List[Ingredient], steps: List[Step], page_address: str = None):
    if page_address is not None:
        recipe.reference = page_address

    recipe.save()

    for ingredient in ingredients:
        if not ingredient.pk:
            ingredient.recipe = recipe
            ingredient.save()
    for step in steps:
        if not step.pk:
            step.recipe = recipe
            step.save()

    recipe.steps.set(steps)
    recipe.ingredients.set(ingredients)

    return recipe


def calculate_recipe_total_time(total: int) -> str:
    if total < 60:
        return f"{total / 100:.2f}"

    hours = total // 60
    minutes = total % 60
    return f"{hours}.{minutes:02}"


def flatten(nested_list):
    """Recursively flattens a deeply nested list."""
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            if flat_list:  # Add a comma before appending a nested list
                flat_list.append(", ")
            flat_list.extend(flatten(item))  # Recursive call for deeper lists
        else:
            flat_list.append(item)
    return flat_list


def delete_files(files: List[Union[str, Path]]):
    for file in files:
        file_path = Path(file)
        try:
            if file_path.exists():
                file_path.unlink()
                print(f"Deleted: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except PermissionError:
            print(f"Permission denied: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")


def delete_json_files_in_paths(file_paths: List):
    local_files_to_delete = [local for local, _ in file_paths if ".json" in local]
    delete_files(local_files_to_delete)


def get_first_file_from_zip_file_folder(zip_file, all_files, folder_path):
    try:
        file_path = next(f for f in all_files if f.startswith(folder_path) and not f.endswith('/'))
        with zip_file.open(file_path) as f:
            return ContentFile(f.read(), name=os.path.basename(file_path))
    except StopIteration:
        return None
