import json
import os
import uuid
from pathlib import Path
from typing import List
from openai import OpenAI

from ..models import PromptType, Recipe
from .prompts import prompt_recipe_main_info, prompt_recipe_instructions, prompt_recipe_ingredients, \
    prompt_generate_recipe, prompt_translate_recipe, prompt_tts_audio
from markdownify import markdownify as md
from dotenv import load_dotenv

load_dotenv()


# TODO:// make it singleton
def __init_open_ai_client():
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return client


def openai_tts_stream(chunks: list, recipe_name: str, language: str):
    client = __init_open_ai_client()
    chunk_files = []

    for i, chunk in enumerate(chunks):
        chunk_file = Path(__file__).parent.parent.parent / f"media/audio/chunks/chunk_{i}.mp3"

        with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=os.getenv("OPEN_AI_TTS_MODEL_VOICE"),
                input=chunk,
                instructions=prompt_tts_audio.format(language)
        ) as response:
            with open(chunk_file, "wb") as f:
                for chunk_data in response.iter_bytes():
                    f.write(chunk_data)

        chunk_files.append(chunk_file)

    file_name = f"{uuid.uuid4()}-{recipe_name.replace(" ", "_")}.mp3"
    speech_file_path = Path(__file__).parent.parent.parent / f"media/audio/{file_name}"

    with open(speech_file_path, "wb") as final_file:
        for file in chunk_files:
            with open(file, "rb") as f:
                final_file.write(f.read())

    return file_name, chunk_files


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
