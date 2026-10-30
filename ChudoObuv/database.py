"""Работа с базой данных: все SQL-запросы приложения собраны здесь."""
import psycopg2
import psycopg2.extras

from config import DB_SETTINGS


class DatabaseError(Exception):
    """Понятная пользователю ошибка работы с БД."""


def open_connection():
    """Открывает соединение с PostgreSQL или бросает DatabaseError."""
    try:
        return psycopg2.connect(**DB_SETTINGS)
    except psycopg2.Error as error:
        raise DatabaseError(
            "Не удалось подключиться к базе данных.\n"
            "Проверьте, что PostgreSQL запущен, а параметры в config.py верны.\n\n"
            f"Подробности: {error}"
        ) from error


def run_query(sql, params=None):
    """Выполняет SELECT и возвращает список словарей."""
    connection = open_connection()
    try:
        with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
    except psycopg2.Error as error:
        raise DatabaseError(f"Ошибка выполнения запроса: {error}") from error
    finally:
        connection.close()


def find_user_by_login(login):
    """Возвращает пользователя (с названием роли) по логину или None."""
    rows = run_query(
        """SELECT u.user_id, u.last_name, u.first_name, u.middle_name, u.login, r.role_name
           FROM users u JOIN roles r ON r.role_id = u.role_id
           WHERE LOWER(u.login) = LOWER(%s)""",
        (login,),
    )
    return rows[0] if rows else None


def load_catalog():
    """Каталог моделей: данные модели, суммарное количество по размерам
    и признак наличия заказов в ПРЕДЫДУЩЕМ календарном месяце (для скидки)."""
    return run_query(
        """SELECT p.product_id, c.category_name, p.product_name, m.manufacturer_name,
                  p.composition, p.price, p.image_path,
                  COALESCE((SELECT SUM(s.quantity_available) FROM stock_items s
                            WHERE s.product_id = p.product_id), 0) AS total_quantity,
                  EXISTS (SELECT 1 FROM order_items oi
                          JOIN orders o ON o.order_id = oi.order_id
                          WHERE oi.product_id = p.product_id
                            AND o.order_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '1 month'
                            AND o.order_date <  date_trunc('month', CURRENT_DATE)
                         ) AS had_orders_last_month
           FROM products p
           JOIN categories c ON c.category_id = p.category_id
           JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
           ORDER BY p.product_name"""
    )
