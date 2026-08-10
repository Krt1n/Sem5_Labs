
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time


message = input("Enter message: ")

des_key = b"12345678"
aes_key = b"0123456789ABCDEF0123456789ABCDEF"

data = message.encode()
iterations = 10000


# DES Encryption
des_iv = get_random_bytes(8)

start = time.perf_counter()

for i in range(iterations):
    cipher = DES.new(des_key, DES.MODE_CBC, des_iv)
    des_ciphertext = cipher.encrypt(pad(data, 8))

des_encrypt_time = (time.perf_counter() - start) / iterations


# DES Decryption
start = time.perf_counter()

for i in range(iterations):
    cipher = DES.new(des_key, DES.MODE_CBC, des_iv)
    des_plaintext = unpad(cipher.decrypt(des_ciphertext), 8)

des_decrypt_time = (time.perf_counter() - start) / iterations


# AES-256 Encryption
aes_iv = get_random_bytes(16)

start = time.perf_counter()

for i in range(iterations):
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    aes_ciphertext = cipher.encrypt(pad(data, 16))

aes_encrypt_time = (time.perf_counter() - start) / iterations


# AES-256 Decryption
start = time.perf_counter()

for i in range(iterations):
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    aes_plaintext = unpad(cipher.decrypt(aes_ciphertext), 16)

aes_decrypt_time = (time.perf_counter() - start) / iterations


# Convert seconds to microseconds
des_encrypt = des_encrypt_time * 1000000
des_decrypt = des_decrypt_time * 1000000

aes_encrypt = aes_encrypt_time * 1000000
aes_decrypt = aes_decrypt_time * 1000000


# Print table
print("\nPerformance Comparison")
print("-" * 65)

print(f"{'Algorithm':<15}{'Encryption (µs)':<20}{'Decryption (µs)':<20}")
print("-" * 65)

print(f"{'DES':<15}{des_encrypt:<20.3f}{des_decrypt:<20.3f}")
print(f"{'AES-256':<15}{aes_encrypt:<20.3f}{aes_decrypt:<20.3f}")

print("-" * 65)


# Implications
print("\nImplications:")

if des_encrypt < aes_encrypt:
    print("- DES was faster for encryption in this test.")
else:
    print("- AES-256 was faster for encryption in this test.")

if des_decrypt < aes_decrypt:
    print("- DES was faster for decryption in this test.")
else:
    print("- AES-256 was faster for decryption in this test.")

print("- DES is obsolete because it has an effective key size of only 56 bits.")
print("- AES-256 provides much stronger security with a 256-bit key.")
print("- AES-256 is recommended for modern applications.")

"""
OUTPUT:

Performance Comparison
-----------------------------------------------------------------
Algorithm      Encryption (µs)     Decryption (µs)     
-----------------------------------------------------------------
DES            6.147               6.137               
AES-256        4.413               4.549               
-----------------------------------------------------------------

Implications:
- AES-256 was faster for encryption in this test.
- AES-256 was faster for decryption in this test.
- DES is obsolete because it has an effective key size of only 56 bits.
- AES-256 provides much stronger security with a 256-bit key.
- AES-256 is recommended for modern applications.
"""