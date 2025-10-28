import re
import unittest

from src.lab1.calculator import check_sequence, tokenize


def eval_expr(expr):
    """Вспомогательная функция для безопасного вычисления через eval с проверкой токенов."""
    tokens = tokenize(expr)
    check_sequence(tokens)
    if re.search(r"[*/%+\-]\s*-\s*\d", expr):
        raise ValueError("Отрицательное число должно быть в скобках")
    return eval(expr)


class CalculatorTestCase(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(eval_expr("1 + 2"), 3)
        self.assertEqual(eval_expr("10 + 0"), 10)

    def test_subtraction(self):
        self.assertEqual(eval_expr("5 - 3"), 2)
        self.assertEqual(eval_expr("0 - 5"), -5)

    def test_multiplication(self):
        self.assertEqual(eval_expr("4 * 3"), 12)
        self.assertEqual(eval_expr("-3 * 5"), -15)

    def test_division(self):
        self.assertEqual(eval_expr("10 / 2"), 5)
        self.assertEqual(eval_expr("7 / 2"), 3.5)

    def test_integer_division(self):
        self.assertEqual(eval_expr("10 // 3"), 3)
        self.assertEqual(eval_expr("7 // 2"), 3)

    def test_modulo(self):
        self.assertEqual(eval_expr("10 % 3"), 1)
        self.assertEqual(eval_expr("7 % 2"), 1)

    def test_power(self):
        self.assertEqual(eval_expr("2 ** 3"), 8)
        self.assertEqual(eval_expr("4 ** 0.5"), 2.0)

    def test_parentheses(self):
        self.assertEqual(eval_expr("(2 + 3) * 4"), 20)
        self.assertEqual(eval_expr("2 + (3 * 4)"), 14)
        self.assertEqual(eval_expr("((2 + 3) * (1 + 1))"), 10)

    def test_unary_minus(self):
        self.assertEqual(eval_expr("-3 + 5"), 2)
        self.assertEqual(eval_expr("-(2 + 3)"), -5)
        self.assertEqual(eval_expr("(-3) * (-2)"), 6)

    def test_negative_in_brackets(self):
        self.assertEqual(eval_expr("3 * (-5)"), -15)
        self.assertEqual(eval_expr("(-3) + 5"), 2)
        with self.assertRaises(ValueError):
            eval_expr("3 * -5")
        with self.assertRaises(ValueError):
            eval_expr("(-3) * -5")

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            eval_expr("5 / 0")
        with self.assertRaises(ZeroDivisionError):
            eval_expr("5 // 0")
        with self.assertRaises(ZeroDivisionError):
            eval_expr("5 % 0")

    def test_invalid_expressions(self):
        with self.assertRaises(ValueError):
            eval_expr("10 + - + 3")
        with self.assertRaises(ValueError):
            eval_expr("10 + 8 * + 3")
        with self.assertRaises(ValueError):
            eval_expr("5 ** -2")  # отрицательная степень без скобок
        with self.assertRaises(ValueError):
            eval_expr("3 ** -1")

    def test_mixed_numbers(self):
        self.assertEqual(eval_expr("2.5 + 3.5"), 6.0)
        self.assertEqual(eval_expr("5.0 // 2"), 2.0)
        self.assertEqual(eval_expr("7.5 % 2"), 1.5)

    def test_complex_expression(self):
        expr = "((2 + 3) * 2 - 5) ** 2 // 3 % 4"
        self.assertEqual(eval_expr(expr), 0)
        expr2 = "((1 + 2) * (3 + 4) - 5) / 2"
        self.assertEqual(eval_expr(expr2), 8.0)


if __name__ == "__main__":
    unittest.main()
