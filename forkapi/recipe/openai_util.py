from dis import Instruction
from typing import List

from django.core.files import File
from playwright.sync_api import sync_playwright
import os
from openai import OpenAI
from dotenv import load_dotenv
from markdownify import markdownify as md
import json
from .models import PromptType, Recipe, Ingredient, Step
from .util import download_media_files, delete_media_file

load_dotenv()

prompt_recipe_main_info = """
            Your goal is to find the elements in the page source that represent the recipe main info and return them in valid json format. 
            Output json:
            
            { "name": "The title or name of the recipe as string", "servings": "The servings (only number as integer)", "description": "The description of the recipe", "image": "Image src path", "video" "Video source path (if available), "difficulty": "string one of 'Easy', 'Intermediate', 'Advanced' or 'Expert'", "chef": "The chef of the recipe", "prep_time": "preparation time in minutes integer value", "cook_time": "The cook time in minutes integer" }

            Make sure to return a plain json dict object with the values found on the page source as described.
            If no data is available return empty json as:
            {}
            Or if field is missing return null for value.
            """

prompt_recipe_instructions = """ 
            Your goal is to find the instructions of the recipe in the provided page source and return them as list of json objects
            Output json:

            [ { "text": "Instruction value start from first" }, { "text": "Second instruction value" }, {"text": "Third instruction value"} ]"

            You must combine all instructions from the page source at the single list of json objects.
            If no data is available return empty json as:
            {}
            """


prompt_recipe_ingredients = """
            Your goal is to find the ingredients of the recipe in the provided page source and return them as list of json objects
            Output json:

            [ { "name": "Full text of the ingredient name", "quantity": "an string value of the quantity if the ingredient", "metric": "the metric of the ingredient eg. g, ml, pcs etc." } , { "name": "Full text of the second ingredient name", "quantity": "an string value of the quantity if the second ingredient", "metric": "the metric of the second ingredient eg. g, ml, pcs etc." } ]"

            You must combine all ingredients from the page source at the single list of json objects.
            If no data is available return empty json as:
            {}
            """

def get_page_content(url: str) -> str | None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        response = page.goto(url=url)
        content = response.text()
        browser.close()

        return content



def __init_open_ai_client():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return client


def __open_ai_message(page_content:str, prompt_type:PromptType):
    client = __init_open_ai_client()
    markdown_content = md(page_content)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that convert markdown page content to a valid json."},
            {
                "role": "user",
                "content": f"Provided markdown: {markdown_content}. Your task is to {prompt_recipe_main_info if prompt_type is PromptType.MAIN_INFO 
                else prompt_recipe_ingredients if prompt_type is PromptType.INGREDIENTS 
                else prompt_recipe_instructions if prompt_type is PromptType.INSTRUCTIONS 
                else prompt_recipe_main_info}.",
            }
        ],
        model=os.getenv("OPENAI_MODEL"),
    )

    return chat_completion.choices[0].message.content


def __parse_recipe_info(json_response:str):
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

def scrape_recipe(content: str):
    # Main info of the recipe
    json_response = __open_ai_message(content, PromptType.MAIN_INFO)
    json_content_main_info = __parse_recipe_info(json_response)
    file_path = manage_media(json_content_main_info, False)

    recipe = Recipe(**json_content_main_info)
    with open(file_path, 'rb') as doc_file:
        recipe.image.save("test", File(doc_file), save=True)

    recipe.save()

    delete_media_file(file_path)

    if json_content_main_info['video']:
        file_path = manage_media(json_content_main_info, True)
        recipe.video = open(file_path, 'rb')
        recipe.save()
        delete_media_file(file_path)

    # Instruction of the recipe
    json_response = __open_ai_message(content, PromptType.INSTRUCTIONS)
    json_content_instructions = __parse_recipe_info(json_response)
    steps = []

    for instruction in json_content_instructions:
        step = Step(**instruction)
        steps.append(step)

    # Ingredients of the recipe
    json_response = __open_ai_message(content, PromptType.INGREDIENTS)
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



