"""Модуль тестирования шифра Цезаря.
Проверяются:
- Шифрование с дефолтным сдвигом
- Шифрование с разными сдвигами
- Шифрование/дешифрование сообщений с цифрами и спецсимволами
- Расшифровка сообщений
- Цикл шифрования и расшифровки
"""

import unittest

# Вспомогательные функции, которые мы тестируем
from src.lab2.caesar import decrypt_caesar, encrypt_caesar


class CaesarCipherTestCase(unittest.TestCase):
    def test_encrypt_default_shift(self):
        """Проверка шифрования с дефолтным сдвигом (3)."""
        self.assertEqual(encrypt_caesar("PYTHON"), "SBWKRQ")
        self.assertEqual(encrypt_caesar("python"), "sbwkrq")
        self.assertEqual(encrypt_caesar("Python 3.9.13"), "Sbwkrq 3.9.13")
        self.assertEqual(encrypt_caesar(""), "")

    def test_encrypt_various_shifts(self):
        """Проверка шифрования с разными сдвигами."""
        self.assertEqual(encrypt_caesar("ABC", 1), "BCD")
        self.assertEqual(encrypt_caesar("XYZ", 3), "ABC")
        self.assertEqual(encrypt_caesar("abc", 2), "cde")
        self.assertEqual(encrypt_caesar("xyz", 4), "bcd")

    def test_encrypt_nonalpha_characters(self):
        """Символы, не являющиеся буквами, не шифруются."""
        self.assertEqual(encrypt_caesar("Hello, World! 123", 5), "Mjqqt, Btwqi! 123")

    def test_decrypt_default_shift(self):
        """Проверка расшифровки с дефолтным сдвигом (3)."""
        self.assertEqual(decrypt_caesar("SBWKRQ"), "PYTHON")
        self.assertEqual(decrypt_caesar("sbwkrq"), "python")
        self.assertEqual(decrypt_caesar("Sbwkrq 3.9.13"), "Python 3.9.13")
        self.assertEqual(decrypt_caesar(""), "")

    def test_decrypt_various_shifts(self):
        """Проверка расшифровки с разными сдвигами."""
        self.assertEqual(decrypt_caesar("BCD", 1), "ABC")
        self.assertEqual(decrypt_caesar("ABC", 3), "XYZ")
        self.assertEqual(decrypt_caesar("cde", 2), "abc")
        self.assertEqual(decrypt_caesar("bcd", 4), "xyz")

    def test_encrypt_decrypt_cycle(self):
        """Проверка корректности шифрования и последующей расшифровки."""
        messages = [
            "HELLO",
            "hello",
            "Python 3.9.13",
            "We are responsible for those who have tamed!",
            "",
            "1234567890!@#$%^&*()",
        ]
        shifts = [0, 1, 3, 5, 10, 7]
        for msg, shift in zip(messages, shifts):
            encrypted = encrypt_caesar(msg, shift)
            decrypted = decrypt_caesar(encrypted, shift)
            self.assertEqual(decrypted, msg)
