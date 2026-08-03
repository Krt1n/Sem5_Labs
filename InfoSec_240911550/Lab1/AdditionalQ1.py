def additive_decrypt(ciphertext, key):
    plaintext = ""
    for ch in ciphertext:
        if ch.isalpha():
            # Determine if uppercase or lowercase
            base = ord('A') if ch.isupper() else ord('a')
            c = ord(ch) - base
            p = (c - key) % 26
            plaintext += chr(p + base)
        else:
            plaintext += ch
    return plaintext

# Ciphertext provided
ciphertext = "NCJAEZRCLAS/LYODEPRLYZRCLASJLCPEHZDTOPDZOLN&BY"

# Alice's birthday is on the 13th, so we test keys close to 13
potential_keys = range(10, 17)

print("--- Brute-Force Attack Results (Keys close to 13) ---")
for key in potential_keys:
    decrypted_msg = additive_decrypt(ciphertext, key)
    print(f"Key {key:2d}: {decrypted_msg}")