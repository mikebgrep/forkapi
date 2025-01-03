import os

import requests


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
