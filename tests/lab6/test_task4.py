"""Модуль с unit-тестами для декоратора call_limiter из задания 4."""

import unittest

from src.lab6.task4 import call_limiter


class TestCallLimiterDecorator(unittest.TestCase):
    """Тесты для декоратора call_limiter."""

    def test_limited_method_calls_within_limit(self):
        """Проверяет, что метод можно вызвать limit раз без ошибок."""

        @call_limiter(limit=2)
        class Calculator:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки вызовов в пределах лимита."""

            def add(self, a, b):
                """Складывает два числа."""
                return a + b

        calc = Calculator()
        self.assertEqual(calc.add(1, 2), 3)
        self.assertEqual(calc.add(3, 4), 7)

    def test_limited_method_exceeds_limit(self):
        """Проверяет, что при превышении лимита выбрасывается RuntimeError."""

        @call_limiter(limit=1)
        class Counter:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки превышения лимита."""

            def inc(self, x):
                """Увеличивает число на 1."""
                return x + 1

        obj = Counter()
        self.assertEqual(obj.inc(5), 6)
        with self.assertRaises(RuntimeError) as ctx:
            obj.inc(10)
        self.assertIn("exceeded call limit of 1", str(ctx.exception))

    def test_separate_counters_for_different_instances(self):
        """Проверяет, что счётчики вызовов разделены для разных экземпляров."""

        @call_limiter(limit=1)
        class Greeter:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки раздельных счётчиков экземпляров."""

            def say_hello(self, name):
                """Возвращает приветствие."""
                return f"Hello, {name}"

        obj1 = Greeter()
        obj2 = Greeter()

        self.assertEqual(obj1.say_hello("Alice"), "Hello, Alice")
        self.assertEqual(obj2.say_hello("Bob"), "Hello, Bob")
        with self.assertRaises(RuntimeError):
            obj1.say_hello("Charlie")

    def test_separate_counters_for_different_methods(self):
        """Проверяет, что счётчики разделены для разных методов."""

        @call_limiter(limit=2)
        class Multi:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки раздельных счётчиков методов."""

            def add(self, a, b):
                """Складывает два числа."""
                return a + b

            def mul(self, a, b):
                """Умножает два числа."""
                return a * b

        obj = Multi()
        self.assertEqual(obj.add(1, 2), 3)
        self.assertEqual(obj.mul(2, 3), 6)
        self.assertEqual(obj.add(3, 4), 7)
        self.assertEqual(obj.mul(4, 5), 20)
        with self.assertRaises(RuntimeError):
            obj.add(5, 6)
        with self.assertRaises(RuntimeError):
            obj.mul(5, 6)

    def test_invalid_limit_non_positive(self):
        """Проверяет, что при передаче неправильного лимита выбрасывается ValueError."""

        with self.assertRaises(ValueError):
            @call_limiter(limit=0)
            class Dummy:  # pylint: disable=unused-variable,too-few-public-methods
                """Класс-заглушка для проверки нулевого лимита."""

                def do_nothing(self):
                    """Пустой метод."""

        with self.assertRaises(ValueError):
            @call_limiter(limit=-5)
            class Dummy2:  # pylint: disable=unused-variable,too-few-public-methods
                """Класс-заглушка для проверки отрицательного лимита."""

                def do_nothing(self):
                    """Пустой метод."""

    def test_invalid_limit_not_int(self):
        """Проверяет, что при передаче не целого числа выбрасывается ValueError."""

        with self.assertRaises(ValueError):
            @call_limiter(limit=2.5)
            class Dummy:  # pylint: disable=unused-variable,too-few-public-methods
                """Класс-заглушка для проверки лимита с плавающей точкой."""

                def do_nothing(self):
                    """Пустой метод."""

        with self.assertRaises(ValueError):
            @call_limiter(limit="2")
            class Dummy2:  # pylint: disable=unused-variable,too-few-public-methods
                """Класс-заглушка для проверки лимита со строкой."""

                def do_nothing(self):
                    """Пустой метод."""

    def test_metadata_preserved(self):
        """Проверяет, что декоратор сохраняет имя и документацию метода."""

        @call_limiter(limit=3)
        class Processor:  # pylint: disable=too-few-public-methods
            """Класс-заглушка для проверки сохранения метаданных."""

            def process(self, value):
                """Удваивает значение."""
                return value * 2

        self.assertEqual(Processor.process.__name__, "process")
        self.assertEqual(Processor.process.__doc__, "Удваивает значение.")

    def test_static_methods_not_limited(self):
        """
        Проверяет, что статические методы не обёртываются и не ограничиваются
        (так как мы используем types.FunctionType, статические методы игнорируются).
        """

        @call_limiter(limit=1)
        class Utility:  # pylint: disable=too-few-public-methods
            """Класс-заглушка со статическим методом."""

            @staticmethod
            def get_answer():
                """Возвращает ответ на главный вопрос."""
                return 42

        self.assertEqual(Utility.get_answer(), 42)
        self.assertEqual(Utility.get_answer(), 42)

    def test_class_methods_not_limited(self):
        """
        Проверяет, что классовые методы не обёртываются и не ограничиваются.
        """

        @call_limiter(limit=1)
        class Factory:  # pylint: disable=too-few-public-methods
            """Класс-заглушка с классовым методом."""

            @classmethod
            def create(cls, name):
                """Создаёт объект с именем."""
                return f"Created {name}"

        self.assertEqual(Factory.create("A"), "Created A")
        self.assertEqual(Factory.create("B"), "Created B")


if __name__ == "__main__":
    unittest.main()
