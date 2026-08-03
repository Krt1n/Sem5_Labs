import math
ciphertext = "XPALASXYFGFUKPXUSOGEUTKCDGEXANMGNVS"
# Find all valid affine keys
valid_a = []
for a in range(26):
    if math.gcd(a, 26) == 1:
        valid_a.append(a)

def decrypt_affine(ciphertext, a, b):
    plaintext = ""
    # modular inverse of a
    a_inv = pow(a, -1, 26)
    for ch in ciphertext:
        if ch.isalpha():
            c = ord(ch) - ord('A')
            p = (a_inv * (c - b)) % 26
            plaintext += chr(p + ord('A'))
        else:
            plaintext += ch

    return plaintext

# Brute force all possible keys
for a in valid_a:
    for b in range(26):
        plaintext = decrypt_affine(ciphertext, a, b)

        print("a =", a, "b =", b, ":", plaintext)