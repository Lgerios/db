# Чудо Обувь — система заказа обуви (учебный проект ДЭ 09.02.07)

Технологии: Python 3 + tkinter (интерфейс), Pillow (картинки), PostgreSQL (БД), psycopg2.

## Запуск
1. `createdb chudo_obuv` и `psql -d chudo_obuv -f database/chudo_obuv.sql` (создаёт таблицы и загружает данные).
2. Параметры подключения — в `config.py` (или переменные окружения `CHUDO_DB_*`).
3. `pip install -r requirements.txt`, затем `python main.py`.

## Что где
- `main.py` — окно и переключение страниц; `config.py` — настройки, цвета, шрифт;
- `database.py` — SQL-запросы; `pricing.py` — цена со скидкой 25% (нет заказов в прошлом месяце);
- `ui/login_page.py` — вход по логину / как гость; `ui/catalog_page.py` — каталог, кнопка «Назад», ФИО справа;
- `resources/images/` — **сюда класть фото моделей** (имя = `products.image_path`); нет фото → `resources/picture.png`.
