# db
Вариант А: через pgAdmin (проще)

Откройте pgAdmin и введите пароль.
Правой кнопкой по Databases → Create → Database. Назовите её chudo_obuv и сохраните.
Правой кнопкой по chudo_obuv → Query Tool.
Нажмите значок папки (Open File) и выберите database\chudo_obuv.sql.
Нажмите ▶ (F5). Внизу должно появиться «Query returned successfully». Таблицы и данные создадутся сами.

Вариант Б: через командную строку

cd "C:\Program Files\PostgreSQL\16\bin"
createdb -U postgres chudo_obuv
psql -U postgres -d chudo_obuv -f "C:\Проекты\ChudoObuv\database\chudo_obuv.sql"

Номер версии (16) у вас может быть другим. Пароль спросят дважды.

Шаг 3. Указать пароль от БД

Откройте config.py и найдите строку "password": os.getenv("CHUDO_DB_PASSWORD", "postgres"). Замените "postgres" на ваш пароль, который задавали при установке PostgreSQL. Остальное (host localhost, port 5432, имя chudo_obuv, user postgres) обычно менять не нужно.

Шаг 4. Установить библиотеки

Откройте командную строку в папке проекта. Для этого зайдите в папку ChudoObuv, нажмите на адресную строку, введите cmd и Enter. Затем выполните:

pip install -r requirements.txt
Шаг 5. Запустить приложение
python main.py

Откроется окно входа. Введите логин, например isivanov (администратор), papetrov (менеджер) или asidorova (авторизованный пользователь). Пароль не нужен. Можно нажать «Войти как гость». В каталоге в правом верхнем углу видно ФИО, а кнопка «Назад» возвращает на вход.

Если вы работаете в PyCharm или VS Code, откройте папку ChudoObuv, откройте файл main.py и нажмите Run.
Модуль 5 (анализ)
Откройте командную строку в папке Module5.
Выполните pip install pandas.
Выполните python analysis.py.
