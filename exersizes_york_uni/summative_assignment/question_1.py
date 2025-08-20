def encrypt(plaintext, key):
    """
    Encrypts a message using the Gear cipher.

    The function filters out non-alphabetic characters from the plaintext,
    converts everything to uppercase, and encrypts the result using the
    provided alphabetic key. The ciphertext is grouped into blocks of 
    5 characters for readability.

    Args:
        plaintext (str): The message to be encrypted. 
            Non-alphabetic characters are ignored.
        key (str): The encryption key, which must contain only letters (A–Z or a–z).

    Raises:
        ValueError: If either `plaintext` or `key` is empty, or if the `key` 
            contains non-alphabetic characters.
        TypeError: If `plaintext` or `key` is not a string.

    Returns:
        str: The encrypted ciphertext in uppercase, grouped into 5-letter blocks.

    Example:
        >>> encrypt("Attack at dawn!", "LEMON")
        'LXFOP VEFRN HR'
    """
    
    if not isinstance(plaintext, str) or not isinstance(key, str):
        raise TypeError("Plaintext and key must be strings.")
    
    if not plaintext or not key:
        raise ValueError("Plaintext and key must not be empty.")

    if not (key.isalpha() and key.isascii()):
        raise ValueError("Key must only contain ASCII letters (A–Z).")
    
    

    plaintext = ''.join(ch for ch in plaintext.upper() if ch.isalpha() and ch.isascii())
    if not plaintext:
        raise ValueError("Plaintext must contain at least one ASCII letter (A–Z).")
    
    repeated_key = (key.upper() * ((len(plaintext) // len(key)) + 1))[:len(plaintext)]
    # full repetitions of the key + 1 in case the key doesn’t divide evenly
    # trimed to be the same length as the plaintext
    
    encrypted = []
    
    for p, k in zip(plaintext, repeated_key):
        shifted = ((ord(p) - 65) + (ord(k) - 65)) % 26
        # turns letters into numbers (A=0 to Z=25), add them
        # uses % 26 to wrap around (since there are 26 letters)
        # ord('A') = 65
        encrypted.append(chr(shifted + 65))
        
    cipher_text = ''.join(encrypted)
    return ' '.join(cipher_text[i:i+5] for i in range(0, len(cipher_text), 5))
    
    
def decrypt(ciphertext, key):
    """
    Decrypts a message encrypted with the Gear cipher.

    The function removes non-alphabetic characters from the ciphertext,
    converts everything to uppercase, and decrypts it using the provided
    alphabetic key. The decrypted message is returned in uppercase
    without spaces or punctuation.

    Args:
        ciphertext (str): The encrypted message to decrypt. 
            Non-alphabetic characters are ignored.
        key (str): The decryption key, which must contain only letters (A–Z or a–z).

    Raises:
        ValueError: If either `ciphertext` or `key` is empty, or if the `key`
            contains non-alphabetic characters.
        TypeError: If `ciphertext` or `key` is not a string.

    Returns:
        str: The decrypted plaintext in uppercase with no spacing.

    Example:
        >>> decrypt("LXFOP VEFRN HR", "LEMON")
        'ATTACKATDAWN'
    """
    
    if not isinstance(ciphertext, str) or not isinstance(key, str):
        raise TypeError("Ciphertext and key must be strings.")
    
    if not ciphertext or not key:
        raise ValueError("Ciphertext and key must not be empty.")

    if not (key.isalpha() and key.isascii()):
        raise ValueError("Key must only contain ASCII letters (A–Z).")
    
    

    ciphertext = ''.join(ch for ch in ciphertext.upper() if ch.isalpha() and ch.isascii())
    if not ciphertext:
        raise ValueError("Ciphertext must contain at least one ASCII letter (A–Z).")
    
    repeated_key = (key.upper() * ((len(ciphertext) // len(key)) + 1))[:len(ciphertext)]
    decrypted = []
    for p, k in zip(ciphertext, repeated_key):
        shifted_back = ((ord(p) - 65) - (ord(k) - 65)) % 26
        decrypted.append(chr(shifted_back + 65))
    
    return ''.join(decrypted)


assert encrypt("Attack at dawn!", "LEMON") == "LXFOP VEFRN HR"
assert encrypt("Hello, World!", "KEY") == "RIJVS UYVJN"
assert encrypt("Hello, World!", "key") == "RIJVS UYVJN"
try:
    encrypt("Hello123, World!", "KEY12")
except ValueError:
    pass  
else:
    raise AssertionError("Expected ValueError for non-alphabetic key")

try:
    encrypt("", "KEY")
except ValueError: pass
else: raise AssertionError("Empty plaintext should raise ValueError")

for bad in ["ñЖ", "Ж", "ééé", "¡¡¡", "123!!!"]:
    try:
        encrypt(bad, "KEY")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError when no ASCII letters remain")



assert decrypt("LXFOP VEFRN HR", "LEMON") == "ATTACKATDAWN"
assert decrypt("RIJVS UYVJN", "KEY") == "HELLOWORLD"
assert decrypt("rijvs uyvjn", "key") == "HELLOWORLD"  # lowercase + spaces tolerated


try:
    decrypt("RIJVS UYVJN", "KEY12")
except ValueError:
    pass
else:
    raise AssertionError("Expected ValueError for non-alphabetic key")


try:
    decrypt("", "KEY")
except ValueError:
    pass
else:
    raise AssertionError("Empty ciphertext should raise ValueError")


try:
    decrypt(12345, "KEY")
except TypeError:
    pass
else:
    raise AssertionError("Non-string ciphertext should raise TypeError")

try:
    decrypt("RIJVS UYVJN", None)
except TypeError:
    pass
else:
    raise AssertionError("Non-string key should raise TypeError")

for bad in ["ñЖ", "Ж", "ééé", "¡¡¡", "123!!!"]:
    try:
        decrypt(bad, "KEY")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError when no ASCII letters remain")