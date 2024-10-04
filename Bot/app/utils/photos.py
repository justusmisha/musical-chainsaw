import os

from aiogram.types import InputMediaPhoto


async def load_photos():
    base_path = os.path.dirname(__file__)
    photo_paths = [
        os.path.join(base_path, '..', 'data', 'static', 'photos', f'photo{i}.jpeg') for i in range(1, 6)
    ]

    media_group = []
    for path in photo_paths:
        if os.path.exists(path):
            media_group.append(InputMediaPhoto(media=open(path, 'rb'), parse_mode=None))
        else:
            print(f"Photo not found: {path}")

    return media_group
