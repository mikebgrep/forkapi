import json
import re
from traceback import print_tb
from typing import List, Tuple

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import URLValidator

from .messages import open_ai_scrape_message, open_ai_generate_recipe_message, open_ai_translate_recipe_message, \
    openai_tts_stream
from ..models import PromptType, Recipe, Ingredient, Step, AudioInstructions
from .browser import Browser
from ..utils import delete_file, get_first_matching_link, remove_stop_words, \
    extract_link_from_duckduck_go_url_result, instructions_and_steps_json_to_lists, parse_recipe_info, manage_media, flatten, \
    delete_files

blacklist = ['foodnetwork.co.uk', 'foodnetwork.com', 'foodnetwork']


def generate_recipes(ingredients: List[str]):
    json_response = open_ai_generate_recipe_message(ingredients)
    json_content_recipes = parse_recipe_info(json_response)
    filtered_recipes = []

    browser = Browser()

    # TODO:// Return multiple recipes from json_content_recipes if have more than one link per recipe name
    for single_recipe_json in json_content_recipes:
        recipe_name = single_recipe_json['name']
        print(recipe_name)
        hrefs = browser.get_duckduckgo_result(url=f"https://duckduckgo.com/html/?q={recipe_name.replace(' ', '%20')}")

        if not hrefs:
            continue

        recipe_words = remove_stop_words(recipe_name)
        link_with_recipe = get_first_matching_link(recipe_words, hrefs)

        if link_with_recipe:
            # Skip if the link is in blacklist
            if any(bl in link_with_recipe for bl in blacklist):
                continue

            val = URLValidator()
            try:
                url = extract_link_from_duckduck_go_url_result(link_with_recipe)
                val(url)
                single_recipe_json['url'] = url
            except (ValidationError, AttributeError) as ex:
                print(ex)
                continue

            if url:
                content, meta_content_thumbnail = browser.get_page_content_recipe(url)
                try:
                    val(meta_content_thumbnail)
                    single_recipe_json['thumbnail'] = meta_content_thumbnail
                except ValidationError as ex:
                    print(ex)
                    continue
        else:
            continue
        filtered_recipes.append(single_recipe_json)

    browser.close()

    return filtered_recipes


def scrape_recipe(url: str):
    if any(item in url for item in blacklist):
        return None, None, None

    browser = Browser()
    content, meta_content_thumbnail = browser.get_page_content_recipe(url)
    browser.close()
    # TODO: meta_content_thumbnail sometimes return 404 on download retry for original image when scraping the recipe
    # https://sweetcaramelsunday.com/beef-pesto-pasta/
    if not content:
        return None, None, None

    # Main info of the recipe
    json_response = open_ai_scrape_message(content, PromptType.MAIN_INFO)
    json_content_main_info = parse_recipe_info(json_response)

    # Edge case when the content contains more than one recipe after the prompt
    try:
        json_content_main_info['image']
    except TypeError as ex:
        print(ex)
        return None, None, None

    if meta_content_thumbnail:
        json_content_main_info['image'] = meta_content_thumbnail.split("?")[0] if \
            len(meta_content_thumbnail.split("?")) > 1 else meta_content_thumbnail

    file_path = manage_media(json_content_main_info, False)

    recipe = Recipe(**json_content_main_info)
    file_name = json_content_main_info['name'].replace("/", "")

    with open(file_path, 'rb') as img_file:
        recipe.image.save(f'{file_name}.png', File(img_file), save=True)
        delete_file(file_path)

    if json_content_main_info['video'] and not 'youtube' in json_content_main_info['video']:
        file_path = manage_media(json_content_main_info, True)
        with open(file_path, 'rb') as video_file:
            recipe.video.save(f'{file_name}.mp4', File(video_file), save=True)
            delete_file(file_path)

    recipe.save()

    # Instruction of the recipe
    json_response = open_ai_scrape_message(content, PromptType.INSTRUCTIONS)
    json_content_instructions = parse_recipe_info(json_response)

    # Ingredients of the recipe
    json_response = open_ai_scrape_message(content, PromptType.INGREDIENTS)
    json_content_ingredients = parse_recipe_info(json_response)

    steps, ingredients = instructions_and_steps_json_to_lists(json_content_instructions, json_content_ingredients)

    return recipe, ingredients, steps


def translate_recipe_to_language(recipe: Recipe, language: str):
    json_response = open_ai_translate_recipe_message(recipe, language)
    print(json_response)
    json_content = parse_recipe_info(json_response)

    name_translated = json_content['name']
    description_translated = json_content['description']
    ingredients_translated = json_content['ingredients']
    instructions_translated = json_content['steps']

    return name_translated, description_translated, ingredients_translated, instructions_translated


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


def translate_and_save_recipe(recipe: Recipe, language: str) -> Recipe | None:
    if any([x for x in recipe.get_variations if x.language == language]):
        return None

    name_translated, description_translated, ingredients_translated, instructions_translated = \
        translate_recipe_to_language(recipe, language)

    steps, ingredients = instructions_and_steps_json_to_lists(instructions_translated, ingredients_translated)

    from copy import deepcopy
    new_recipe = deepcopy(recipe)
    new_recipe.pk = None
    new_recipe.name = name_translated
    new_recipe.description = description_translated
    new_recipe.original_recipe_pk = recipe.pk
    new_recipe.language = language

    #TODO:// Saving image and video to new file if one of the copies is deleted
    new_recipe.image.save(f"{recipe.name.replace(" ", "_")}.png", recipe.image)
    if recipe.video:
        new_recipe.video.save(f"{recipe.name.replace(" ", "_")}.mp4", recipe.video)


    translated_recipe = save_recipe(new_recipe, ingredients, steps)

    return translated_recipe


def recipe_to_tts_audio(recipe: Recipe):
    formated_result = {
        "name": recipe.name,
        "ingredients": [[i.quantity, i.metric, i.name] for i in recipe.ingredients.all()],
        "instructions": [step.text for step in recipe.steps.all()]
    }

    sentences = []
    [sentences.extend([k,v]) for k,v in formated_result.items()]
    chunks = split_recipe_json_to_sentences(sentences)

    file_name, chunk_files = openai_tts_stream(chunks, recipe.name, recipe.language)
    audio_instructions = AudioInstructions.objects.create(file=f"audio/{file_name}", recipe=recipe)
    delete_files(chunk_files)

    return audio_instructions

def split_recipe_json_to_sentences(sentences):
    """
    Function to split the recipe json to smaller chunks so openai tts to not made nonce`s responses
    """
    chunks = []
    max_char_limit = 300
    current_chunk = ""
    flat_sentences = flatten(sentences)

    for sentence in flat_sentences:
        words = sentence.split()
        for word in words:
            current_chunk += word + " "
            if len(current_chunk) >= max_char_limit:
                chunks.append(current_chunk)
                current_chunk = ""

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
