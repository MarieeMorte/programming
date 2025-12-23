"""
Модуль для обработки заказов онлайн-магазина продуктов.
"""

import re
from collections import Counter
from typing import Dict, List, Optional

ERROR_ADDRESS = 1
ERROR_PHONE = 2

PRIORITY_ORDER = {"MAX": 0, "MIDDLE": 1, "LOW": 2}


def validate_address(address: str) -> bool:
    """Проверка адреса доставки"""
    if not address.strip():
        return False

    parts = address.split(". ")
    if len(parts) != 4:
        return False

    return all(part.strip() for part in parts)


def validate_phone(phone: str) -> bool:
    """Проверка номера телефона"""
    if not phone.strip():
        return False

    pattern = r"^\+\d-\d{3}-\d{3}-\d{2}-\d{2}$"
    return bool(re.match(pattern, phone))


def parse_order(line: str) -> Optional[dict[str, str]]:
    """Парсинг строки заказа"""
    parts = line.strip().split(";")
    if len(parts) != 6:
        return None

    cleaned_parts = [part.strip() for part in parts]

    if not cleaned_parts[0]:
        return None

    return {
        "order_id": cleaned_parts[0],
        "products": cleaned_parts[1],
        "customer_name": cleaned_parts[2],
        "address": cleaned_parts[3],
        "phone": cleaned_parts[4],
        "priority": cleaned_parts[5],
    }


def process_products(products_str: str) -> str:
    """Обработка набора продуктов с подсчетом количества"""
    products = [p.strip() for p in products_str.split(",") if p.strip()]

    if not products:
        return ""

    counter: Counter[str] = Counter()
    seen_order = []

    for product in products:
        counter[product] += 1
        if product not in seen_order:
            seen_order.append(product)

    result = []
    for product in seen_order:
        count = counter[product]
        if count > 1:
            result.append(f"{product} x{count}")
        else:
            result.append(product)

    return ", ".join(result)


def format_address(address: str) -> str:
    """Форматирование адреса (удаление страны)"""
    parts = address.split(". ")
    if len(parts) == 4:
        return ". ".join(parts[1:])
    return address


def get_country_from_address(address: str) -> str:
    """Извлечение страны из адреса"""
    parts = address.split(". ")
    return parts[0] if parts else ""


def sort_orders(orders: List[Dict]) -> List[Dict]:
    """Сортировка заказов по стране и приоритету"""

    def sort_key(order):
        country = get_country_from_address(order["address"])

        if "Россия" in country or "Российская Федерация" in country:
            country_order = 0
            country_name = "Россия"
        else:
            country_order = 1
            country_name = country

        priority_value = PRIORITY_ORDER.get(order["priority"], 3)

        return country_order, country_name, priority_value, order["order_id"]

    return sorted(orders, key=sort_key)


def main() -> None:
    """Основная функция обработки заказов."""
    valid_orders = []
    errors = []

    try:
        with open("orders.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Файл orders.txt не найден!")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue

        order = parse_order(line)
        if not order:
            continue

        order_id = order["order_id"]

        if not order["address"] or not validate_address(order["address"]):
            error_value = "no data" if not order["address"] else order["address"]
            errors.append((order_id, ERROR_ADDRESS, error_value))

        if not order["phone"] or not validate_phone(order["phone"]):
            error_value = "no data" if not order["phone"] else order["phone"]
            errors.append((order_id, ERROR_PHONE, error_value))

        if validate_address(order["address"]) and validate_phone(order["phone"]):
            valid_orders.append(order)

    with open("non_valid_orders.txt", "w", encoding="utf-8") as file:
        for order_id, error_type, error_value in errors:
            file.write(f"{order_id};{error_type};{error_value}\n")

    if valid_orders:
        sorted_orders = sort_orders(valid_orders)

        with open("order_country.txt", "w", encoding="utf-8") as file:
            for order in sorted_orders:
                products_formatted = process_products(order["products"])
                address_formatted = format_address(order["address"])

                line = (
                    f"{order['order_id']};{products_formatted};{order['customer_name']};"
                    f"{address_formatted};{order['phone']};{order['priority']}"
                )
                file.write(line + "\n")
    else:
        with open("order_country.txt", "w", encoding="utf-8"):
            pass

    print("Обработка завершена!")
    print(f"Валидных заказов: {len(valid_orders)}")
    print(f"Найдено ошибок: {len(errors)}")


if __name__ == "__main__":
    main()
