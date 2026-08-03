"""Encrypt the message "the house is being sold tonight" using one of the following ciphers.
Ignore the space between words.
Decrypt the message to get the original plaintext:
• Vigenere cipher with key: "dollars"
• Autokey cipher with key = 7"""

def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ","").upper()
    key = key.upper()

    ciphertext = ""
    key_index = 0
    for ch in plaintext:
        if ch.isalpha():
            p = ord(ch) - ord('A')
            k = ord(key[key_index % len(key)]) - ord('A')
            c = (p+k)%26
            ciphertext += chr(c+ord('A'))
            key_index += 1
        else:
            ciphertext += ch
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()
    key = key.upper()

    plaintext = ""
    key_index = 0

    for ch in ciphertext:
        if ch.isalpha():
            c = ord(ch) - ord('A')
            k = ord(key[key_index % len(key)]) - ord('A')
            p = (c - k) % 26
            plaintext += chr(p + ord('A'))
            key_index += 1
        else:
            plaintext += ch

    return plaintext

def autokey_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()

    ciphertext = ""

    # First key is numeric, remaining keys come from plaintext
    keystream = [key] + [ord(ch) - ord('A') for ch in plaintext[:-1]]

    for i in range(len(plaintext)):
        p = ord(plaintext[i]) - ord('A')
        c = (p + keystream[i]) % 26
        ciphertext += chr(c + ord('A'))

    return ciphertext

def autokey_decrypt(ciphertext, key):
    ciphertext = ciphertext.upper()

    plaintext = ""
    current_key = key

    for ch in ciphertext:
        c = ord(ch) - ord('A')
        p = (c - current_key) % 26
        plain_char = chr(p + ord('A'))

        plaintext += plain_char

        # Next key is the plaintext just recovered
        current_key = p

    return plaintext

message = input("Enter the message: ")
vig_key = "dollars"
vig_cipher = vigenere_encrypt(message, vig_key)
vig_plain = vigenere_decrypt(vig_cipher, vig_key)

print("\n--- Vigenere Cipher ---")
print("Key        :", vig_key)
print("Ciphertext :", vig_cipher)
print("Decrypted  :", vig_plain)

# Autokey
auto_key = 7
auto_cipher = autokey_encrypt(message, auto_key)
auto_plain = autokey_decrypt(auto_cipher, auto_key)

print("\n--- Autokey Cipher ---")
print("Key        :", auto_key)
print("Ciphertext :", auto_cipher)
print("Decrypted  :", auto_plain)

