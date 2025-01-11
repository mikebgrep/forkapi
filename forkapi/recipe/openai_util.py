from typing import List, Tuple

from django.core.files import File
from playwright.sync_api import sync_playwright
import os
from openai import OpenAI
from dotenv import load_dotenv
from markdownify import markdownify as md
import json

from playwright_stealth import stealth_sync

from .models import PromptType, Recipe, Ingredient, Step
from .util import download_media_files, delete_media_file, get_first_matching_link, remove_stop_words, \
    extract_link_from_duckduck_go_url_result

load_dotenv()

prompt_recipe_main_info = """
            Your goal is to find the elements in the page source that represent the recipe main info and return them in valid json format. 
            Output json:
            
            ```json
            { "name": "The title or name of the recipe as string", "servings": "The servings (only number as integer)", "description": "The description of the recipe", "image": "Image src path", "video" "Video source path (if available), "difficulty": "string one of 'Easy', 'Intermediate', 'Advanced' or 'Expert'", "chef": "The chef of the recipe", "prep_time": "preparation time in minutes integer value", "cook_time": "The cook time in minutes integer" }
            ```
            
            Make sure to return a plain json dict object with the values found on the page source as described.
            If no data is available return empty json as:
            ```json
            {}
            ```
            Or if field is missing return null for value.
            !Note return only the json not conversions!
            """

prompt_recipe_instructions = """ 
            Your goal is to find the instructions of the recipe in the provided page source and return them as list of json objects
            Output json:

            ```json
            [ { "text": "Instruction value start from first" }, { "text": "Second instruction value" }, {"text": "Third instruction value"} ]"
            ```
            
            You must combine all instructions from the page source at the single list of json objects.
            If no data is available return empty json as:
            ```json
            {}
            ```
            !Note return only the json not conversions!
            """

prompt_recipe_ingredients = """
            Your goal is to find the ingredients of the recipe in the provided page source and return them as list of json objects
            Output json:
            
            ```json
            [ { "name": "Full text of the ingredient name", "quantity": "an string value of the quantity if the ingredient", "metric": "the metric of the ingredient eg. g, ml, pcs etc." } , { "name": "Full text of the second ingredient name", "quantity": "an string value of the quantity if the second ingredient", "metric": "the metric of the second ingredient eg. g, ml, pcs etc." } ]"
            ```

            You must combine all ingredients from the page source at the single list of json objects.
            If no data is available return empty json as:
            ```json
            {}
            ```
            !Note return only the json not conversions!
            """

prompt_generate_recipe = """
            Your goal is to generate 5 recipes from the provided ingredients. 
            Output json:
            
            ```json
            [ { "name": "Full name of the recipe"}, .... ]
            ```
            
            You must not make up a recipe names.
            If no data is available return empty json as:
            ```json
            {}
            ```
            !Note return only the json not conversions!
            """


def get_page_content_recipe(url: str) -> Tuple[str, str] | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        stealth_sync(page)
        response = page.goto(url=url)
        # Get thumbnail for recipies without image
        meta_content_thumbnail = page.locator('meta[property="og:image"]').get_attribute('content')
        content = response.text()
        browser.close()

        return content, meta_content_thumbnail


def get_duckduckgo_result(url) -> List[str] | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url=url)
        href_elements = page.locator('a.result__a')
        href_values = href_elements.evaluate_all('elements => elements.map(e => e.href)')
        browser.close()

        return href_values


def __init_open_ai_client():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return client


def __openai_chat_completion(messages):
    client = __init_open_ai_client()

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=os.getenv("OPENAI_MODEL"),
    )

    return chat_completion.choices[0].message.content


def __open_ai_scrape_message(page_content: str, prompt_type: PromptType):
    markdown_content = md(page_content)

    messages = [
        {"role": "system",
         "content": "You are a helpful assistant that convert markdown page content to a valid json."},
        {
            "role": "user",
            "content": f"Provided markdown: {markdown_content}. Your task is to {prompt_recipe_main_info if prompt_type is PromptType.MAIN_INFO
            else prompt_recipe_ingredients if prompt_type is PromptType.INGREDIENTS
            else prompt_recipe_instructions if prompt_type is PromptType.INSTRUCTIONS
            else prompt_recipe_main_info}.",
        }
    ]

    return __openai_chat_completion(messages)


def __open_ai_generate_recipe_message(ingredients: List[str] = None):
    messages = [
        {"role": "system",
         "content": "You are helpful assistant that generate a valid recipes from a given ingredients and return them to a valid json"},
        {
            "role": "user",
            "content": f"With provided ingredients: {ingredients}. Your task is to {prompt_generate_recipe}"
        }
    ]

    return __openai_chat_completion(messages)


def __parse_recipe_info(json_response: str):
    json_response = json_response.replace("```", "").replace("json", "")
    json_content = json.loads(json_response)
    return json_content


def __manage_media(json_content_main_info, is_video: bool):
    image_url = json_content_main_info['image'] if not is_video else json_content_main_info['video']
    file_path = download_media_files(address=image_url, recipe_name=json_content_main_info['name'], is_video=is_video)
    if not is_video:
        del json_content_main_info['image']
    else:
        del json_content_main_info['video']
    return file_path


def generate_recipes(ingredients: List[str]):
    json_response = __open_ai_generate_recipe_message(ingredients)
    json_content_recipes = __parse_recipe_info(json_response)

    for index, single_recipe_json in enumerate(json_content_recipes):
        recipe_name = single_recipe_json['name']
        hrefs = get_duckduckgo_result(url=f"https://duckduckgo.com/html/?q={recipe_name}")
        recipe_words = remove_stop_words(recipe_name)
        link_with_recipe =  get_first_matching_link(recipe_words, hrefs)
        try:
            # TODO:// May be edge case when no exception and the link is missing
            url = extract_link_from_duckduck_go_url_result(link_with_recipe)
            single_recipe_json['url'] = url

            content, meta_content_thumbnail = get_page_content_recipe(url)
            if not meta_content_thumbnail:
                raise AttributeError("No thumbnail found")

            single_recipe_json['thumbnail'] = meta_content_thumbnail
        except AttributeError as ex:
            print(ex)
            del json_content_recipes[index]

    return json_content_recipes


def scrape_recipe(url: str):
    content, meta_content_thumbnail = get_page_content_recipe(url)
    # Main info of the recipe
    json_response = __open_ai_scrape_message(content, PromptType.MAIN_INFO)
    json_content_main_info = __parse_recipe_info(json_response)

    if not json_content_main_info['image']:
        json_content_main_info['image'] = meta_content_thumbnail.split("?")[0]

    file_path = __manage_media(json_content_main_info, False)

    recipe = Recipe(**json_content_main_info)
    file_name = json_content_main_info['name'].replace("/", "")

    with open(file_path, 'rb') as doc_file:
        recipe.image.save(f'{file_name}.png', File(doc_file), save=True)
        delete_media_file(file_path)

    if json_content_main_info['video'] and not 'youtube' in json_content_main_info['video']:
        file_path = __manage_media(json_content_main_info, True)
        with open(file_path, 'rb') as doc_file:
            recipe.video.save(f'{file_name}.mp4', File(doc_file), save=True)
            delete_media_file(file_path)

    recipe.save()

    # Instruction of the recipe
    json_response = __open_ai_scrape_message(content, PromptType.INSTRUCTIONS)
    json_content_instructions = __parse_recipe_info(json_response)
    steps = []

    for instruction in json_content_instructions:
        step = Step(**instruction)
        steps.append(step)

    # Ingredients of the recipe
    json_response = __open_ai_scrape_message(content, PromptType.INGREDIENTS)
    json_content_ingredients = __parse_recipe_info(json_response)

    ingredients = []
    for ingredient in json_content_ingredients:
        ingredient = Ingredient(**ingredient)
        ingredients.append(ingredient)

    return recipe, ingredients, steps


def save_scraped_recipe(recipe: Recipe, ingredients: List[Ingredient], steps: List[Step], page_address: str):
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
