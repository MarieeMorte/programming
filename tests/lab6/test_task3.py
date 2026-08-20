import io
import unittest
from unittest.mock import patch

from src.lab6.task3 import logger


class TestLoggerClassDecorator(unittest.TestCase):

    def test_logging_all_methods_including_magic(self):
        """Проверяем, что логируются все методы, включая магические."""

        @logger(show_magic_methods=True)
        class TestClass:
            def __init__(self, x):
                self.x = x

            def method(self, y):
                return self.x + y

            def __str__(self):
                return f"Test({self.x})"

            def __add__(self, other):
                return TestClass(self.x + other.x)

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            obj = TestClass(10)
            obj.method(5)
            str(obj)
            obj + TestClass(3)
            output = mock_stdout.getvalue()

        self.assertIn("Метод: __init__", output)
        self.assertIn("Метод: method", output)
        self.assertIn("Метод: __str__", output)
        self.assertIn("Метод: __add__", output)
        self.assertIn("Результат: 15", output)
        self.assertIn("Результат: Test(10)", output)

    def test_skip_magic_methods(self):
        @logger(show_magic_methods=False)
        class TestClass:
            def __init__(self, x):
                self.x = x

            def method(self, y):
                return self.x + y

            def __str__(self):
                return f"Test({self.x})"

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            obj = TestClass(10)
            obj.method(5)
            str(obj)
            output = mock_stdout.getvalue()

        self.assertIn("Метод: method", output)
        self.assertNotIn("Метод: __init__", output)
        self.assertNotIn("Метод: __str__", output)

    def test_skip_critical_magic_methods(self):
        """Проверяем, что критические методы (__getattribute__ и др.) не оборачиваются даже если show_magic_methods=True."""

        @logger(show_magic_methods=True)
        class TestClass:
            def __init__(self, x):
                self.x = x

            def __getattribute__(self, name):
                return object.__getattribute__(self, name)

        try:
            obj = TestClass(5)
            self.assertEqual(obj.x, 5)
        except RecursionError:
            self.fail("__getattribute__ был обёрнут, вызвав рекурсию")

    def test_static_methods(self):
        """Проверяем, что статические методы также логируются."""

        @logger(show_magic_methods=True)
        class TestClass:
            @staticmethod
            def static_method(a, b):
                return a + b

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result = TestClass.static_method(3, 4)
            output = mock_stdout.getvalue()
        self.assertEqual(result, 7)
        self.assertIn("Метод: static_method", output)
        self.assertIn("Результат: 7", output)

    def test_class_methods(self):
        """Проверяем, что классовые методы логируются."""

        @logger(show_magic_methods=True)
        class TestClass:
            @classmethod
            def class_method(cls, x):
                return x * 2

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result = TestClass.class_method(5)
            output = mock_stdout.getvalue()
        self.assertEqual(result, 10)
        self.assertIn("Метод: class_method", output)
        self.assertIn("Результат: 10", output)

    def test_preserve_metadata(self):
        """Проверяем, что имя и документация метода сохраняются (благодаря @wraps)."""

        @logger(show_magic_methods=True)
        class TestClass:
            def my_method(self, x):
                """Документация."""
                return x

        self.assertEqual(TestClass.my_method.__name__, "my_method")
        self.assertEqual(TestClass.my_method.__doc__, "Документация.")


if __name__ == "__main__":
    unittest.main()
