"""Тесты для модуля Vigenere cipher.

Проверяются:
- базовое шифрование и дешифрование;
- чувствительность к регистру;
- корректная обработка символов, не являющихся буквами;
- правильная работа с короткими и длинными ключами;
- цикл шифрования-дешифрования.
"""

from src.lab2.vigenre import decrypt_vigenere, encrypt_vigenere


class TestVigenere:
    """Тесты для функций encrypt_vigenere и decrypt_vigenere."""

    def test_encrypt_basic(self):
        """Проверяет базовые примеры шифрования из докстринга."""
        assert encrypt_vigenere("PYTHON", "A") == "PYTHON"
        assert encrypt_vigenere("python", "a") == "python"
        assert encrypt_vigenere("ATTACKATDAWN", "LEMON") == "LXFOPVEFRNHR"

    def test_decrypt_basic(self):
        """Проверяет базовые примеры расшифровки из докстринга."""
        assert decrypt_vigenere("PYTHON", "A") == "PYTHON"
        assert decrypt_vigenere("python", "a") == "python"
        assert decrypt_vigenere("LXFOPVEFRNHR", "LEMON") == "ATTACKATDAWN"

    def test_encrypt_with_nonalpha(self):
        """Проверяет, что символы вне диапазона букв не меняются."""
        result = encrypt_vigenere("Hello, World! 123", "KEY")
        assert result == "Rijvs, Uyvjn! 123"

    def test_case_sensitivity(self):
        """Проверяет корректность работы с разным регистром ключа и текста."""
        assert encrypt_vigenere("Python", "a") == "Python"
        assert encrypt_vigenere("Python", "B") == "Qzuipo"
        assert decrypt_vigenere("Qzuipo", "B") == "Python"

    def test_encrypt_long_keyword(self):
        """Проверяет работу, когда ключ длиннее текста."""
        assert encrypt_vigenere("HELLO", "LONGKEYWORD") == "SSYRY"
        assert decrypt_vigenere("SSYRY", "LONGKEYWORD") == "HELLO"

    def test_encrypt_empty(self):
        """Проверяет корректность работы с пустыми строками."""
        assert encrypt_vigenere("", "KEY") == ""
        assert decrypt_vigenere("", "KEY") == ""

    def test_encrypt_decrypt_cycle(self):
        """Проверяет, что после шифрования и дешифрования получается исходный текст."""
        messages = [
            "HELLO",
            "hello",
            "Python3.10",
            "The quick brown fox jumps over the lazy dog!",
            "",
        ]
        keywords = ["A", "key", "LEMON", "ABC", "xyz"]
        for msg, key in zip(messages, keywords):
            encrypted = encrypt_vigenere(msg, key)
            decrypted = decrypt_vigenere(encrypted, key)
            assert decrypted == msg
