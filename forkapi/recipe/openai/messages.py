import json
import os
import uuid
from pathlib import Path
from typing import List
from openai import OpenAI

from ..models import PromptType, Recipe
from .prompts import prompt_recipe_main_info, prompt_recipe_instructions, prompt_recipe_ingredients, \
    prompt_generate_recipe, prompt_translate_recipe
from markdownify import markdownify as md
from dotenv import load_dotenv

load_dotenv()


# TODO:// make it singleton
def __init_open_ai_client():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return client


def openai_tts_stream(recipe_json: dict, language: str):
    client = __init_open_ai_client()

    with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=os.getenv("OPEN_AI_TTS_MODEL_VOICE"),
            input=str(recipe_json),
            instructions=f"Speak as professional cooking chef assistant with pause of 0.5 sec on each item. You must spell the recipe `name`, the `ingredients` and \
            `instruction` from the provided json string object on the provided language: {language}. \
            Important: You must not skip any ingredient or instruction or mix them also the ingredients \
            must be read with all available information for each of them without skipping nothing! (Pay attention to this).\
            And finish the speach after all are spelled.",
    ) as response:
        file_name = f"{uuid.uuid4()}-{recipe_json['name'].replace(" ", "_")}.mp3"
        speech_file_path = Path(__file__).parent.parent.parent / f"media/audio/{file_name}"
        response.stream_to_file(speech_file_path)

        return file_name


def __openai_chat_completion(messages, model=os.getenv("OPENAI_MODEL")):
    client = __init_open_ai_client()

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )

    return chat_completion.choices[0].message.content


def open_ai_scrape_message(page_content: str, prompt_type: PromptType):
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


def open_ai_generate_recipe_message(ingredients: List[str] = None):
    messages = [
        {"role": "system",
         "content": "You are helpful assistant that generate a valid recipes from a given ingredients and return them to a valid json"},
        {
            "role": "user",
            "content": f"With provided ingredients: {ingredients}. Your task is to {prompt_generate_recipe}"
        }
    ]

    return __openai_chat_completion(messages)


def open_ai_translate_recipe_message(recipe: Recipe, language: str):
    messages = [
        {"role": "system",
         "content": "Your are helpful assistant that translate recipes to foreign languages and return them to a valid json"},
        {
            "role": "user",
            "content": f"With the provided name: {recipe.name}, description: {recipe.description}, ingredients: {json.dumps(list(recipe.ingredients.all().values()))} and instruction/steps: {json.dumps(list(recipe.steps.all().values()))}. Your task it to {prompt_translate_recipe} to the  provided language: {language}"
        }
    ]
    # TODO: Change model if not performing well on translation , model="gpt-4-turbo"
    return __openai_chat_completion(messages)
