"""
Модуль с unit-тестами для декоратора call_limiter из задания 4.
Проверяет ограничение числа вызовов для обычных, статических и классовых методов,
а также работу с наследованием и критическими магическими методами.
"""

import unittest

from src.lab6.task4 import call_limiter


class TestCallLimiter(unittest.TestCase):
    """Тесты для декоратора call_limiter."""

    def test_limit_on_instance_methods(self):
        """Проверяет ограничение для обычных методов (счётчик на экземпляр)."""

        @call_limiter(limit=2)
        class A:  # pylint: disable=too-few-public-methods
            """Внутренний тестовый класс."""

            def method(self):
                """Возвращает 'OK'."""
                return "OK"

        a = A()
        self.assertEqual(a.method(), "OK")
        self.assertEqual(a.method(), "OK")
        with self.assertRaises(RuntimeError) as cm:
            a.method()
        self.assertIn("Call limit (2) exceeded", str(cm.exception))

        b = A()
        self.assertEqual(b.method(), "OK")
        self.assertEqual(b.method(), "OK")
        with self.assertRaises(RuntimeError):
            b.method()

    def test_limit_on_classmethod(self):
        """Проверяет ограничение для классовых методов (счётчик на класс/подкласс)."""

        @call_limiter(limit=3)
        class A:  # pylint: disable=too-few-public-methods
            """Внутренний тестовый класс."""

            @classmethod
            def cm(cls):
                """Возвращает имя класса."""
                return cls.__name__

        self.assertEqual(A.cm(), "A")
        self.assertEqual(A.cm(), "A")
        self.assertEqual(A.cm(), "A")
        with self.assertRaises(RuntimeError):
            A.cm()

        class B(A):  # pylint: disable=too-few-public-methods
            """Подкласс A."""

        self.assertEqual(B.cm(), "B")
        self.assertEqual(B.cm(), "B")
        self.assertEqual(B.cm(), "B")
        with self.assertRaises(RuntimeError):
            B.cm()

        with self.assertRaises(RuntimeError):
            A.cm()

    def test_limit_on_staticmethod(self):
        """Проверяет ограничение для статических методов (общий счётчик на класс)."""

        @call_limiter(limit=1)
        class A:  # pylint: disable=too-few-public-methods
            """Внутренний тестовый класс."""

            @staticmethod
            def sm():
                """Возвращает 'static'."""
                return "static"

        self.assertEqual(A.sm(), "static")
        with self.assertRaises(RuntimeError):
            A.sm()

        class B(A):  # pylint: disable=too-few-public-methods
            """Подкласс A."""

        with self.assertRaises(RuntimeError):
            B.sm()

    def test_skip_critical_magic(self):
        """Проверяет, что критические методы (__getattribute__) не обёртываются."""

        @call_limiter(limit=2)
        class A:  # pylint: disable=too-few-public-methods
            """Внутренний тестовый класс."""

            def __init__(self):
                """Инициализирует атрибут x."""
                self.x = 1

            def __getattribute__(self, name):
                """Переопределённый доступ к атрибутам."""
                return object.__getattribute__(self, name)

        a = A()
        self.assertEqual(a.x, 1)

    def test_limit_zero(self):
        """Проверяет, что при limit=0 любой вызов сразу вызывает исключение."""

        @call_limiter(limit=0)
        class A:  # pylint: disable=too-few-public-methods
            """Внутренний тестовый класс."""

            def method(self):
                """Возвращает 'OK'."""
                return "OK"

        a = A()
        with self.assertRaises(RuntimeError):
            a.method()

    def test_preserve_metadata(self):
        """Проверяет сохранение имени и документации метода (благодаря @wraps)."""

        @call_limiter(limit=1)
        class A:  # pylint: disable=too-few-public-methods
            """Внутренний тестовый класс."""

            def method(self, x):
                """Документация метода."""
                return x

        self.assertEqual(A.method.__name__, "method")
        self.assertEqual(A.method.__doc__, "Документация метода.")


if __name__ == "__main__":
    unittest.main()
