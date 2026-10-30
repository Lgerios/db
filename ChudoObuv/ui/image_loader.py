"""Загрузка картинок с сохранением пропорций (логотип и фото не искажаются)."""
import os

from PIL import Image, ImageTk

import config

_image_cache = {}  # PhotoImage нужно хранить в памяти, иначе tkinter их удалит


def load_scaled_image(path, max_width, max_height):
    """Загружает картинку и вписывает в рамку max_width x max_height БЕЗ искажения."""
    key = (path, max_width, max_height)
    if key not in _image_cache:
        image = Image.open(path)
        image.thumbnail((max_width, max_height), Image.LANCZOS)  # thumbnail сохраняет пропорции
        _image_cache[key] = ImageTk.PhotoImage(image)
    return _image_cache[key]


def load_product_image(image_name, max_width, max_height):
    """Фото модели из resources/images; если файла нет или он битый - заглушка picture.png."""
    path = os.path.join(config.IMAGES_DIR, image_name) if image_name else None
    if path and os.path.isfile(path):
        try:
            return load_scaled_image(path, max_width, max_height)
        except OSError:
            pass  # повреждённый файл - используем заглушку
    return load_scaled_image(config.PLACEHOLDER_PATH, max_width, max_height)
