"""
Use a Hill cipher to encipher the message "We live in an insecure world". Use the following
key:
𝐾 = [03 03 2 07]
"""

def mod_inverse(a, m):
    """Find modular inverse of a under modulo m"""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def matrix_inverse_2x2(key):
    """Calculate inverse of 2x2 matrix modulo 26"""

    a = key[0][0]
    b = key[0][1]
    c = key[1][0]
    d = key[1][1]

    # determinant
    det = (a * d - b * c) % 26

    # inverse of determinant
    det_inv = mod_inverse(det, 26)

    if det_inv is None:
        raise ValueError("Matrix has no inverse modulo 26")

    # Adjoint matrix * determinant inverse
    inverse = [
        [(d * det_inv) % 26, (-b * det_inv) % 26],
        [(-c * det_inv) % 26, (a * det_inv) % 26]
    ]

    return inverse


def hill_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()

    if len(plaintext) % 2 != 0:
        plaintext += "X"

    ciphertext = ""

    for i in range(0, len(plaintext), 2):

        p1 = ord(plaintext[i]) - ord('A')
        p2 = ord(plaintext[i+1]) - ord('A')

        c1 = (key[0][0]*p1 + key[0][1]*p2) % 26
        c2 = (key[1][0]*p1 + key[1][1]*p2) % 26

        ciphertext += chr(c1 + ord('A'))
        ciphertext += chr(c2 + ord('A'))

    return ciphertext


def hill_decrypt(ciphertext, inverse_key):

    plaintext = ""

    for i in range(0, len(ciphertext), 2):

        c1 = ord(ciphertext[i]) - ord('A')
        c2 = ord(ciphertext[i+1]) - ord('A')

        p1 = (inverse_key[0][0]*c1 +
              inverse_key[0][1]*c2) % 26

        p2 = (inverse_key[1][0]*c1 +
              inverse_key[1][1]*c2) % 26

        plaintext += chr(p1 + ord('A'))
        plaintext += chr(p2 + ord('A'))

    return plaintext


# Main

message = input("Enter the message: ")

key = [
    [3, 3],
    [2, 7]
]


inverse_key = matrix_inverse_2x2(key)

ciphertext = hill_encrypt(message, key)

decrypted = hill_decrypt(ciphertext, inverse_key)


print("\n--- Hill Cipher ---")

print("Key Matrix:")
for row in key:
    print(row)

print("\nInverse Key Matrix:")
for row in inverse_key:
    print(row)

print("\nCiphertext :", ciphertext)
print("Decrypted  :", decrypted)
