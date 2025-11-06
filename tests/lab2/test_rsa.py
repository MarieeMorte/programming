"""Тестирование RSA-модуля: проверяются основные функции и корректность шифрования/дешифрования."""
import unittest

from src.lab2.rsa import gcd, is_prime, multiplicative_inverse


class TestRSA(unittest.TestCase):
    """Набор тестов для RSA-модуля."""

    def test_is_prime(self):
        """Проверяет корректность определения простых чисел."""
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(13))
        self.assertTrue(is_prime(101))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(100))

    def test_gcd(self):
        """Проверяет корректность нахождения НОД."""
        self.assertEqual(gcd(451, 287), 41)
        self.assertEqual(gcd(616, 364), 28)
        self.assertEqual(gcd(7975, 2585), 55)
        self.assertEqual(gcd(645, 381), 3)

    def test_multiplicative_inverse(self):
        """Проверяет вычисление мультипликативного обратного элемента."""
        self.assertEqual(multiplicative_inverse(7, 40), 23)
        self.assertEqual(multiplicative_inverse(93, 53), 4)
        self.assertEqual(multiplicative_inverse(3, 11), 4)

        num, mod = 3, 26
        inverse_val = multiplicative_inverse(num, mod)
        self.assertEqual((num * inverse_val) % mod, 1)

        num, mod = 23, 4
        inverse_val = multiplicative_inverse(num, mod)
        self.assertEqual((num * inverse_val) % mod, 1)

        num, mod = 2, 7
        inverse_val = multiplicative_inverse(num, mod)
        self.assertEqual((num * inverse_val) % mod, 1)
