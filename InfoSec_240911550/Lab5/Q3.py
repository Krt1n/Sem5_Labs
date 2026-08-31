# Q3. Compare MD5, SHA-1 and SHA-256.
# Generate 50–100 random strings.
# Measure hashing time and detect collisions for each algorithm.
# Display execution time and number of collisions.

import hashlib
import random
import string
import time

n=int(input("Enter number of strings (50-100:) "))
if n<50 or n>100:
    print("Please enter a number between 50 and 100.")
    exit()

def generate_random_string(length=20):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

data = [generate_random_string() for _ in range(n)]

algorithms = {
    "MD5": hashlib.md5,
    "SHA-1": hashlib.sha1,
    "SHA-256": hashlib.sha256
}

print("Hashing Performance")
print("-"*50)

for name,algorithm in algorithms.items():
    hashes = []
    start_time = time.perf_counter()
    for text in data:
        hash_value = algorithm(text.encode()).hexdigest()
        hashes.append(hash_value)

    end_time = time.perf_counter()

    unique_hashes = set(hashes)
    collisions=len(hashes)-len(unique_hashes)

    execution_time = end_time - start_time
    print("\nAlgorithm: ",name)
    print("Execution Time: ",execution_time,"seconds")
    print("Collisions: ",collisions)

print("\nCollision Resistance:")
print("MD5    - Weak / broken for collision resistance")
print("SHA-1  - Weak / deprecated for collision resistance")
print("SHA-256 - Strong collision resistance")


"""
Sample I/O:

Enter number of strings (50-100:) 69
Hashing Performance
--------------------------------------------------

Algorithm:  MD5
Execution Time:  8.787299975665519e-05 seconds
Collisions:  0

Algorithm:  SHA-1
Execution Time:  3.705000017362181e-05 seconds
Collisions:  0

Algorithm:  SHA-256
Execution Time:  3.470599995125667e-05 seconds
Collisions:  0

Collision Resistance:
MD5    - Weak / broken for collision resistance
SHA-1  - Weak / deprecated for collision resistance
SHA-256 - Strong collision resistance
"""