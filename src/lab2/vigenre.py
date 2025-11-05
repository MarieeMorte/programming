"""Module implementing Vigenere cipher encryption and decryption."""


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_length = len(keyword)
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(keyword[key_index % key_length].lower()) - ord("a")
            if "A" <= char <= "Z":
                ciphertext += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            elif "a" <= char <= "z":
                ciphertext += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            key_index += 1
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_length = len(keyword)
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(keyword[key_index % key_length].lower()) - ord("a")
            if "A" <= char <= "Z":
                plaintext += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            elif "a" <= char <= "z":
                plaintext += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            key_index += 1
        else:
            plaintext += char
    return plaintext
