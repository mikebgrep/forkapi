from typing import List, Tuple

from django.core.files import File
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from playwright.sync_api import sync_playwright, TimeoutError
import os
from openai import OpenAI
from dotenv import load_dotenv
from markdownify import markdownify as md
import json
from playwright_stealth import stealth_sync, StealthConfig

from .models import PromptType, Recipe, Ingredient, Step
from .util import download_media_files, delete_media_file, get_first_matching_link, remove_stop_words, \
    extract_link_from_duckduck_go_url_result, instructions_and_steps_json_to_lists

load_dotenv()

prompt_recipe_main_info = """
            Your goal is to find the elements in the page source that represent the recipe main info and return them in valid json format. 
            Output json:
            
            ```json
            { "name": "The title or name of the recipe as string", "servings": "The servings (only number as integer must not be null)", "description": "The description of the recipe", "image": "Image src path", "video" "Video source path (if available), "difficulty": "string one of 'Easy', 'Intermediate', 'Advanced' or 'Expert'", "chef": "The chef of the recipe", "prep_time": "preparation time in minutes integer value", "cook_time": "The cook time in minutes integer" }
            ```
            
            Make sure to return a plain json dict object with the values found on the page source as described.
            If no data is available return empty json as:
            ```json
            {}
            ```
            Or if field is missing return null for value except the servings.Make sure the image url pointing to a image file not blob or else.
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

prompt_translate_recipe = """
            Your task is to translate the given recipe and return it in structured json format:
            ```json
            { "name": "Translated name string", "description": "Translated description string", "ingredients" : [ { "name": "Full text of the ingredient name", "quantity": "an string value of the quantity if in the ingredient", "metric": "the metric of the ingredient eg. g, ml, pcs etc."}, ... ], "steps" : [{ "text": "Instruction value start from first" }, { "text": "Second instruction value" }, {"text": "Third instruction value"} ]
            ```
            !Note you must translate only the: `name`, `description`, `ingredients` and `steps`
            as described in the json example and the ingredients metrics and quantity should be the correct by the standard of the language.
            """


blacklist = ['foodnetwork.co.uk', 'foodnetwork.com', 'foodnetwork']


def get_page_content_recipe(url: str) -> Tuple[str | None, str | None] | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Changing user agent to Chrome as Cloudflare look for it
        user_agent = page.evaluate("navigator.userAgent")
        user_agent_replaced = user_agent.replace("HeadlessChrome/", "Chrome/")
        context = browser.new_context(
            user_agent=user_agent_replaced
        )

        # Disable navigator configs affect cloudflare with this we are not blocked
        config = StealthConfig(
            navigator_user_agent=False,
            navigator_plugins=False,
            navigator_vendor=False,
        )

        page = context.new_page()
        stealth_sync(page, config=config)
        try:
            response = page.goto(url=url, timeout=7000)
        except TimeoutError as ex:
            print(ex)
            return None, None

        try:
            # Get page content to be sure is captured regarding and issue with Chrome
            content = response.text()
            # Get thumbnail for recipies without image
            meta_content_thumbnail = page.locator('meta[property="og:image"]').nth(0).get_attribute('content',
                                                                                                    timeout=3700)
            browser.close()
        except TimeoutError as ex:
            print(ex)
            browser.close()
            return content, None

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


def __openai_chat_completion(messages, model=os.getenv("OPENAI_MODEL")):
    client = __init_open_ai_client()

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
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

def __open_ai_translate_recipe_message(recipe: Recipe, language: str):
    messages = [
        {"role": "system",
         "content": "Your are helpful assistant that translate recipes to foreign languages and return them to a valid json"},
        {
            "role": "user",
            "content": f"With the provided name: {recipe.name}, description: {recipe.description}, ingredients: {json.dumps(list(recipe.ingredients.all().values()))} and instruction/steps: {json.dumps(list(recipe.steps.all().values()))}. Your task it to {prompt_translate_recipe} to the  provided language: {language}"
        }
    ]
    #TODO: Change model if not performing well on translation , model="gpt-4-turbo"
    return  __openai_chat_completion(messages)


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
    filtered_recipes = []

    # TODO:// Return multiple recipes from json_content_recipes if have more than one link per recipe name
    for single_recipe_json in json_content_recipes:
        recipe_name = single_recipe_json['name']
        hrefs = get_duckduckgo_result(url=f"https://duckduckgo.com/html/?q={recipe_name}")
        recipe_words = remove_stop_words(recipe_name)
        link_with_recipe = get_first_matching_link(recipe_words, hrefs)

        if link_with_recipe:
            val = URLValidator()
            try:
                url = extract_link_from_duckduck_go_url_result(link_with_recipe)
                val(url)
                single_recipe_json['url'] = url
            except (ValidationError, AttributeError) as ex:
                print(ex)
                continue

            if url:
                content, meta_content_thumbnail = get_page_content_recipe(url)
                try:
                    val(meta_content_thumbnail)
                    single_recipe_json['thumbnail'] = meta_content_thumbnail
                except ValidationError as ex:
                    print(ex)
                    continue
        else:
            continue
        filtered_recipes.append(single_recipe_json)

    return filtered_recipes


def scrape_recipe(url: str):
    if any(item in url for item in blacklist):
        return None, None, None

    content, meta_content_thumbnail = get_page_content_recipe(url)
    # TODO: meta_content_thumbnail sometimes return 404 on download retry for original image when scraping the recipe
    # https://sweetcaramelsunday.com/beef-pesto-pasta/
    if not content:
        return None, None, None

    # Main info of the recipe
    json_response = __open_ai_scrape_message(content, PromptType.MAIN_INFO)
    json_content_main_info = __parse_recipe_info(json_response)

    if meta_content_thumbnail:
        json_content_main_info['image'] = meta_content_thumbnail.split("?")[0]

    file_path = __manage_media(json_content_main_info, False)

    recipe = Recipe(**json_content_main_info)
    file_name = json_content_main_info['name'].replace("/", "")

    with open(file_path, 'rb') as img_file:
        recipe.image.save(f'{file_name}.png', File(img_file), save=True)
        delete_media_file(file_path)

    if json_content_main_info['video'] and not 'youtube' in json_content_main_info['video']:
        file_path = __manage_media(json_content_main_info, True)
        with open(file_path, 'rb') as video_file:
            recipe.video.save(f'{file_name}.mp4', File(video_file), save=True)
            delete_media_file(file_path)

    recipe.save()

    # Instruction of the recipe
    json_response = __open_ai_scrape_message(content, PromptType.INSTRUCTIONS)
    json_content_instructions = __parse_recipe_info(json_response)

    # Ingredients of the recipe
    json_response = __open_ai_scrape_message(content, PromptType.INGREDIENTS)
    json_content_ingredients = __parse_recipe_info(json_response)

    steps, ingredients = instructions_and_steps_json_to_lists(json_content_instructions, json_content_ingredients)

    return recipe, ingredients, steps


def translate_recipe_to_language(recipe: Recipe, language: str):
    json_response = __open_ai_translate_recipe_message(recipe, language)
    json_content = __parse_recipe_info(json_response)

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

def translate_and_save_recipe(recipe: Recipe, language: str) -> Recipe:
    name_translated, description_translated, ingredients_translated, instructions_translated = \
        translate_recipe_to_language(recipe, language)

    steps, ingredients = instructions_and_steps_json_to_lists(instructions_translated, ingredients_translated)

    from copy import deepcopy
    new_recipe = deepcopy(recipe)
    new_recipe.pk = None
    new_recipe.name = name_translated
    new_recipe.description = description_translated

    recipe = save_recipe(new_recipe, ingredients, steps)

    return recipe







