import os

from aiogram.types import InputMediaPhoto, InputFile


async def load_photos():
    base_path = os.path.dirname(__file__)
    photo_paths = [
        os.path.join(base_path, '..', 'data', 'static', 'Лепка', f'photo{i}.jpeg') for i in range(1, 6)
    ]

    media_group = []
    for path in photo_paths:
        if os.path.exists(path):
            media_group.append(InputMediaPhoto(media=open(path, 'rb'), parse_mode=None))
        else:
            print(f"Photo not found: {path}")

    return media_group


async def load_school_photos():
    base_path = os.path.dirname(__file__)
    photo_paths = [
        os.path.join(base_path, '..', 'data', 'static', 'school_photos', f'photo{i}.jpeg') for i in range(1, 6)
    ]

    media_group = []
    for path in photo_paths:
        if os.path.exists(path):
            media_group.append(InputMediaPhoto(media=open(path, 'rb'), parse_mode=None))
        else:
            print(f"Photo not found: {path}")

    return media_group


async def get_schedule_photo(day: str):
    photo_path = f'app/data/static/schedule_days/{day}.jpg'

    if os.path.exists(photo_path):
        return InputFile(path_or_bytesio=photo_path)
    else:
        return False
