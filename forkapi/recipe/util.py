import os
from typing import List

import requests
from urllib.parse import unquote

def calculate_recipe_total_time(total: int) -> str:
    if total < 60:
        return f"{total / 100:.2f}"

    hours = total // 60
    minutes = total % 60
    return f"{hours}.{minutes:02}"


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


def delete_media_file(file_path: str):
    os.remove(file_path)


def get_first_matching_link(words: str, strings: List[str]) -> str | None:
    """
        Used to get the first link that contains all the matching recipe words
    """
    for string in strings:
        if all(word.lower() in string for word in words):
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


def extract_link_from_duckduck_go_url_result(url: str) -> str:
    link_with_ext = url.split("?uddg=")[1]
    encoded_url = link_with_ext.split("&rut")[0]

    return unquote(encoded_url)
