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

    for ch in plaintext:
        if ch.isalpha():
            shift = ord(keyword[key_index % key_length].lower()) - ord('a')
            if 'A' <= ch <= 'Z':
                ciphertext += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
            elif 'a' <= ch <= 'z':
                ciphertext += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
            key_index += 1
        else:
            ciphertext += ch
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

    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(keyword[key_index % key_length].lower()) - ord('a')
            if 'A' <= ch <= 'Z':
                plaintext += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
            elif 'a' <= ch <= 'z':
                plaintext += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
            key_index += 1
        else:
            plaintext += ch
    return plaintext
