"""Алгоритм расчёта цены товара с учётом скидки."""
from decimal import Decimal, ROUND_HALF_UP

from config import DISCOUNT_PERCENT


def calculate_price(base_price, had_orders_last_month):
    """Скидка DISCOUNT_PERCENT % действует, если за предыдущий календарный месяц
    на товар не было ни одного заказа. Возвращает цену в рублях (2 знака)."""
    price = Decimal(base_price)
    if not had_orders_last_month:
        price = price * (Decimal(100) - DISCOUNT_PERCENT) / Decimal(100)
    return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
