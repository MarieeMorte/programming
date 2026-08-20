import unittest
from src.lab6.task4 import call_limiter


class TestCallLimiter(unittest.TestCase):

    def test_limit_on_instance_methods(self):
        @call_limiter(limit=2)
        class A:
            def method(self):
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
        @call_limiter(limit=3)
        class A:
            @classmethod
            def cm(cls):
                return cls.__name__

        self.assertEqual(A.cm(), "A")
        self.assertEqual(A.cm(), "A")
        self.assertEqual(A.cm(), "A")
        with self.assertRaises(RuntimeError):
            A.cm()

        class B(A):
            pass

        self.assertEqual(B.cm(), "B")
        self.assertEqual(B.cm(), "B")
        self.assertEqual(B.cm(), "B")
        with self.assertRaises(RuntimeError):
            B.cm()

        with self.assertRaises(RuntimeError):
            A.cm()

    def test_limit_on_staticmethod(self):
        @call_limiter(limit=1)
        class A:
            @staticmethod
            def sm():
                return "static"

        self.assertEqual(A.sm(), "static")
        with self.assertRaises(RuntimeError):
            A.sm()

        class B(A):
            pass

        with self.assertRaises(RuntimeError):
            B.sm()

    def test_skip_critical_magic(self):
        @call_limiter(limit=2)
        class A:
            def __init__(self):
                self.x = 1

            def __getattribute__(self, name):
                return object.__getattribute__(self, name)

        a = A()
        self.assertEqual(a.x, 1)

    def test_limit_zero(self):
        @call_limiter(limit=0)
        class A:
            def method(self):
                return "OK"

        a = A()
        with self.assertRaises(RuntimeError):
            a.method()

    def test_preserve_metadata(self):
        @call_limiter(limit=1)
        class A:
            def method(self, x):
                """Документация метода."""
                return x

        self.assertEqual(A.method.__name__, "method")
        self.assertEqual(A.method.__doc__, "Документация метода.")


if __name__ == "__main__":
    unittest.main()
