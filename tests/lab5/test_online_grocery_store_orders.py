"""
Модульные тесты для обработчика заказов онлайн-магазина.
"""

import os
import shutil
import tempfile
import unittest

from src.lab5.online_grocery_store_orders import (
    ERROR_ADDRESS,
    ERROR_PHONE,
    PRIORITY_ORDER,
    format_address,
    get_country_from_address,
    main,
    parse_order,
    process_products,
    sort_orders,
    validate_address,
    validate_phone,
)


class TestValidateAddress(unittest.TestCase):
    """Тесты для функции validate_address"""

    def test_valid_address(self):
        """Тест корректного адреса"""
        self.assertTrue(validate_address("Россия. Московская область. Москва. улица Ленина"))
        self.assertTrue(validate_address("США. Калифорния. Лос-Анджелес. Голливудский бульвар"))

    def test_invalid_address(self):
        """Тест некорректного адреса"""
        self.assertFalse(validate_address(""))
        self.assertFalse(validate_address("   "))
        self.assertFalse(validate_address("Россия. Москва"))
        self.assertFalse(validate_address("Россия. Москва. ул Ленина"))
        self.assertFalse(validate_address("Россия. Москва. . д. 10"))
        self.assertFalse(validate_address("Россия..Москва. ул. Ленина"))


class TestValidatePhone(unittest.TestCase):
    """Тесты для функции validate_phone"""

    def test_valid_phone(self):
        """Тест корректного номера телефона"""
        self.assertTrue(validate_phone("+7-123-456-78-90"))
        self.assertTrue(validate_phone("+1-234-567-89-01"))

    def test_invalid_phone(self):
        """Тест некорректного номера телефона"""
        self.assertFalse(validate_phone(""))
        self.assertFalse(validate_phone("   "))
        self.assertFalse(validate_phone("7-123-456-78-90"))
        self.assertFalse(validate_phone("+7-123-456-7890"))
        self.assertFalse(validate_phone("+33-123-456-78-90"))


class TestParseOrder(unittest.TestCase):
    """Тесты для функции parse_order"""

    def test_valid_order_parsing(self):
        """Тест корректного разбора заказа"""
        result = parse_order(
            "1;яблоки, бананы;Иван Иванов;"
            "Россия. Московская область. Москва. улица Ленина;+7-123-456-78-90;MIDDLE"
        )
        expected = {
            "order_id": "1",
            "products": "яблоки, бананы",
            "customer_name": "Иван Иванов",
            "address": "Россия. Московская область. Москва. улица Ленина",
            "phone": "+7-123-456-78-90",
            "priority": "MIDDLE",
        }
        self.assertEqual(result, expected)

    def test_order_with_spaces(self):
        """Тест заказа с пробелами"""
        result = parse_order(
            "  1 ; яблоки ; Иван ; "
            "Россия. Московская область. Москва. улица Ленина ; +7-123-456-78-90 ; MIDDLE  "
        )
        expected = {
            "order_id": "1",
            "products": "яблоки",
            "customer_name": "Иван",
            "address": "Россия. Московская область. Москва. улица Ленина",
            "phone": "+7-123-456-78-90",
            "priority": "MIDDLE",
        }
        self.assertEqual(result, expected)

    def test_invalid_order_format(self):
        """Тест некорректного формата заказа"""
        self.assertIsNone(parse_order("1;яблоки;Иван"))
        self.assertIsNone(parse_order("1;яблоки;Иван;Россия;+7-123-456-78-90;MIDDLE;extra"))
        self.assertIsNone(parse_order(""))
        self.assertIsNone(parse_order(" ;яблоки;Иван;Россия;+7-123-456-78-90;MIDDLE"))


class TestProcessProducts(unittest.TestCase):
    """Тесты для функции process_products"""

    def test_single_products(self):
        """Тест уникальных продуктов"""
        self.assertEqual(process_products("яблоки, бананы, апельсины"), "яблоки, бананы, апельсины")

    def test_duplicate_products(self):
        """Тест повторяющихся продуктов"""
        self.assertEqual(
            process_products("яблоки, бананы, яблоки, апельсины, бананы"),
            "яблоки x2, бананы x2, апельсины",
        )

    def test_products_with_spaces(self):
        """Тест продуктов с пробелами"""
        self.assertEqual(process_products("  яблоки , бананы  , яблоки  "), "яблоки x2, бананы")

    def test_edge_cases(self):
        """Тест граничных случаев"""
        self.assertEqual(process_products(""), "")
        self.assertEqual(process_products("яблоки"), "яблоки")
        self.assertEqual(process_products("яблоки, яблоки"), "яблоки x2")
        self.assertEqual(process_products(", , яблоки, , "), "яблоки")


class TestFormatAddress(unittest.TestCase):
    """Тесты для функции format_address"""

    def test_format_valid_address(self):
        """Тест форматирования корректного адреса"""
        self.assertEqual(
            format_address("Россия. Московская область. Москва. улица Ленина"),
            "Московская область. Москва. улица Ленина",
        )

    def test_format_invalid_address(self):
        """Тест форматирования некорректного адреса"""
        self.assertEqual(format_address("Москва. ул. Ленина"), "Москва. ул. Ленина")
        self.assertEqual(format_address("Россия"), "Россия")
        self.assertEqual(format_address(""), "")
        self.assertEqual(format_address("Россия. Москва"), "Россия. Москва")


class TestGetCountryFromAddress(unittest.TestCase):
    """Тесты для функции get_country_from_address"""

    def test_get_country_valid(self):
        """Тест извлечения страны из корректного адреса"""
        self.assertEqual(
            get_country_from_address("Россия. Московская область. Москва. улица Ленина"), "Россия"
        )

    def test_get_country_invalid(self):
        """Тест извлечения страны из некорректного адреса"""
        self.assertEqual(get_country_from_address("Москва. ул. Ленина"), "Москва")
        self.assertEqual(get_country_from_address(""), "")
        self.assertEqual(get_country_from_address("Россия"), "Россия")


class TestSortOrders(unittest.TestCase):
    """Тесты для функции sort_orders"""

    def test_sort_by_priority_within_same_country(self):
        """Тест сортировки по приоритету внутри одной страны"""
        orders = [
            {
                "order_id": "1",
                "products": "яблоки",
                "customer_name": "Иван",
                "address": "Россия. Московская область. Москва. улица Ленина",
                "phone": "+7-123-456-78-90",
                "priority": "LOW",
            },
            {
                "order_id": "2",
                "products": "бананы",
                "customer_name": "Петр",
                "address": "Россия. Московская область. Москва. улица Ленина",
                "phone": "+7-123-456-78-90",
                "priority": "MAX",
            },
            {
                "order_id": "3",
                "products": "апельсины",
                "customer_name": "Анна",
                "address": "Россия. Московская область. Москва. улица Ленина",
                "phone": "+7-123-456-78-90",
                "priority": "MIDDLE",
            },
        ]

        sorted_orders = sort_orders(orders)
        order_ids = [order["order_id"] for order in sorted_orders]
        self.assertEqual(order_ids, ["2", "3", "1"])

    def test_sort_with_russian_federation(self):
        """Тест сортировки с 'Российская Федерация'"""
        orders = [
            {
                "order_id": "1",
                "products": "виноград",
                "customer_name": "Алексей",
                "address": "Российская Федерация. Татарстан. Казань. улица Кремлевская",
                "phone": "+7-111-222-33-44",
                "priority": "MAX",
            },
            {
                "order_id": "2",
                "products": "яблоки",
                "customer_name": "Иван",
                "address": "Германия. Бавария. Мюнхен. Мариенплац",
                "phone": "+1-234-567-89-01",
                "priority": "MAX",
            },
        ]

        sorted_orders = sort_orders(orders)
        order_ids = [order["order_id"] for order in sorted_orders]
        self.assertEqual(order_ids, ["1", "2"])


class TestMainFunctionIntegration(unittest.TestCase):
    """Интеграционные тесты для основной функции"""

    def setUp(self):
        """Создание временной директории для тестов"""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Очистка временной директории"""
        os.chdir(self.original_dir)

        shutil.rmtree(self.test_dir)

    def test_main_with_valid_orders(self):
        """Тест основной функции с валидными заказами"""
        test_data = """1;яблоки, бананы;Иван Иванов;
        Россия. Московская область. Москва. улица Ленина;+7-123-456-78-90;MIDDLE
        2;апельсины, яблоки, апельсины;Петр Петров;
        США. Калифорния. Лос-Анджелес. Голливудский бульвар;+1-234-567-89-01;MAX
        3;молоко, хлеб, молоко;Анна Сидорова;
        Российская Федерация. Татарстан. Казань. улица Кремлевская;+7-987-654-32-10;LOW"""

        with open("orders.txt", "w", encoding="utf-8") as file:
            file.write(test_data)

        main()

        self.assertTrue(os.path.exists("order_country.txt"))
        self.assertTrue(os.path.exists("non_valid_orders.txt"))

        with open("order_country.txt", "r", encoding="utf-8") as file:
            result_lines = file.readlines()

        self.assertEqual(len(result_lines), 3)

        self.assertTrue("1;" in result_lines[0] or "3;" in result_lines[0])
        self.assertTrue("1;" in result_lines[1] or "3;" in result_lines[1])
        self.assertTrue("2;" in result_lines[2])

    def test_main_with_invalid_orders(self):
        """Тест основной функции с невалидными заказами"""
        test_data = """1;яблоки;Иван;Россия. Московская область;+7-123-456-78-90;MIDDLE
2;бананы;Петр;Россия. Московская область. Москва. улица Ленина;invalid-phone;MAX
3;апельсины;Анна;;+7-987-654-32-10;LOW
4;груши;Мария;Россия. Московская область. Москва. улица Ленина;+7-111-222-33-44;MIDDLE
"""

        with open("orders.txt", "w", encoding="utf-8") as file:
            file.write(test_data)

        main()

        self.assertTrue(os.path.exists("non_valid_orders.txt"))

        with open("non_valid_orders.txt", "r", encoding="utf-8") as file:
            error_lines = file.readlines()

        self.assertEqual(len(error_lines), 3)

        with open("order_country.txt", "r", encoding="utf-8") as file:
            valid_lines = file.readlines()

        self.assertEqual(len(valid_lines), 1)
        self.assertIn("4;", valid_lines[0])


class TestConstants(unittest.TestCase):
    """Тесты для констант"""

    def test_error_constants(self):
        """Тест значений констант ошибок"""
        self.assertEqual(ERROR_ADDRESS, 1)
        self.assertEqual(ERROR_PHONE, 2)

    def test_priority_order(self):
        """Тест словаря приоритетов"""
        self.assertEqual(PRIORITY_ORDER, {"MAX": 0, "MIDDLE": 1, "LOW": 2})


if __name__ == "__main__":
    unittest.main(verbosity=2)
