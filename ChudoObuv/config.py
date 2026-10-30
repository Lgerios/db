"""Настройки приложения: подключение к БД, пути к ресурсам, цвета и шрифты (Приложение 3)."""
import os

APP_NAME = "Чудо Обувь"  # название компании-заказчика должно быть в названии приложения

# --- Подключение к PostgreSQL (можно переопределить переменными окружения) ---
DB_SETTINGS = {
    "host": os.getenv("CHUDO_DB_HOST", "localhost"),
    "port": int(os.getenv("CHUDO_DB_PORT", "5432")),
    "dbname": os.getenv("CHUDO_DB_NAME", "chudo_obuv"),
    "user": os.getenv("CHUDO_DB_USER", "postgres"),
    "password": os.getenv("CHUDO_DB_PASSWORD", "123624"),
}

# --- Ресурсы ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
# КУДА ДОБАВЛЯТЬ КАРТИНКИ ТОВАРОВ: в папку resources/images.
# Имя файла должно совпадать со значением products.image_path в БД (например IMG_KS_195217.png).
IMAGES_DIR = os.path.join(RESOURCES_DIR, "images")
PLACEHOLDER_PATH = os.path.join(RESOURCES_DIR, "picture.png")  # заглушка, если фото нет
LOGO_PATH = os.path.join(RESOURCES_DIR, "logo.png")            # логотип (не искажать!)
ICON_PATH = os.path.join(RESOURCES_DIR, "icon.ico")            # иконка приложения

# --- Руководство по стилю ---
FONT_FAMILY = "Calibri"
COLOR_MAIN_BG = "#FFFFFF"      # основной фон
COLOR_EXTRA_BG = "#D2F6E7"     # дополнительный фон
COLOR_ACCENT = "#70B2AF"       # акцент (кнопки целевых действий)
COLOR_LOW_STOCK = "#ff8080"    # подсветка товаров с количеством <= 3

LOW_STOCK_LIMIT = 3            # порог подсветки (суммарно по всем размерам)
DISCOUNT_PERCENT = 25          # скидка на товары без заказов за прошлый месяц
