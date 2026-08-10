from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time

message = input("Enter message: ")

# DES key = 8 bytes
des_key = b"12345678"

# AES-256 key = 32 bytes
aes_key = b"0123456789ABCDEF0123456789ABCDEF"

# Number of times to run each operation
iterations = 10000

# Convert message to bytes
data = message.encode()

# DES Encryption
des_iv = get_random_bytes(8)

start = time.perf_counter()

for i in range(iterations):
    cipher = DES.new(des_key, DES.MODE_CBC, des_iv)
    des_ciphertext = cipher.encrypt(pad(data, DES.block_size))

end = time.perf_counter()

des_encrypt_time = (end - start) / iterations



# DES Decryption
start = time.perf_counter()

for i in range(iterations):
    cipher = DES.new(des_key, DES.MODE_CBC, des_iv)
    des_decrypted = unpad(cipher.decrypt(des_ciphertext),DES.block_size)

end = time.perf_counter()

des_decrypt_time = (end - start) / iterations

# AES-256 Encryption
aes_iv = get_random_bytes(16)

start = time.perf_counter()

for i in range(iterations):
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    aes_ciphertext = cipher.encrypt(pad(data, AES.block_size))

end = time.perf_counter()

aes_encrypt_time = (end - start) / iterations

# AES-256 Decryption
start = time.perf_counter()

for i in range(iterations):
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    aes_decrypted = unpad(
        cipher.decrypt(aes_ciphertext),
        AES.block_size
    )

end = time.perf_counter()

aes_decrypt_time = (end - start) / iterations

# Convert to microseconds
des_encrypt_us = des_encrypt_time * 1_000_000
des_decrypt_us = des_decrypt_time * 1_000_000

aes_encrypt_us = aes_encrypt_time * 1_000_000
aes_decrypt_us = aes_decrypt_time * 1_000_000

# Display Results

print("\n----------------------------------------")
print("      ENCRYPTION PERFORMANCE TEST")
print("----------------------------------------")

print("Message:", message)
print("Iterations:", iterations)

print("\nDES:")
print("Average Encryption Time :",
      round(des_encrypt_us, 3), "microseconds")

print("Average Decryption Time :",
      round(des_decrypt_us, 3), "microseconds")

print("\nAES-256:")
print("Average Encryption Time :",
      round(aes_encrypt_us, 3), "microseconds")

print("Average Decryption Time :",
      round(aes_decrypt_us, 3), "microseconds")

# Comparison
print("\n----------------------------------------")
print("             COMPARISON")
print("----------------------------------------")

if des_encrypt_time < aes_encrypt_time:
    print("Encryption: DES is faster")
else:
    print("Encryption: AES-256 is faster")

if des_decrypt_time < aes_decrypt_time:
    print("Decryption: DES is faster")
else:
    print("Decryption: AES-256 is faster")

print("\nDES Encryption Ciphertext:")
print(des_ciphertext.hex().upper())
print("\nAES-256 Encryption Ciphertext:")
print(aes_ciphertext.hex().upper())

# Verification
if des_decrypted.decode() == message:
    print("\nDES Decryption: Successful")
else:
    print("\nDES Decryption: Failed")


if aes_decrypted.decode() == message:
    print("AES-256 Decryption: Successful")
else:
    print("AES-256 Decryption: Failed")

