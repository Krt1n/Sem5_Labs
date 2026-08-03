"""
Known Plaintext Attack:
Attacker knows cipher text as well as the corresponding plain text
"""

def find_shift(plaintext, ciphertext):
    plaintext = plaintext.upper()
    ciphertext = ciphertext.upper()

    # Calculate shift using the first character
    shift = (ord(ciphertext[0]) - ord(plaintext[0])) % 26
    return shift

def decrypt_caesar(ciphertext, shift):
    ciphertext = ciphertext.upper()
    plaintext = ""

    for ch in ciphertext:
        if ch.isalpha():
            p = (ord(ch) - ord('A') - shift) % 26
            plaintext += chr(p + ord('A'))
        else:
            plaintext += ch

    return plaintext

# Main
known_cipher = input("Enter known ciphertext: ")
known_plain = input("Enter known plaintext: ")
new_cipher = input("Enter ciphertext to decrypt: ")

shift = find_shift(known_plain, known_cipher)
decrypted = decrypt_caesar(new_cipher, shift)

print("\n--- Known Plaintext Attack ---")
print("Attack Type : Known-Plaintext Attack")
print("Shift Key   :", shift)
print("Plaintext   :", decrypted)


