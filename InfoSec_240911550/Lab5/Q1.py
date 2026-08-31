# Q1. Implement a hash function starting with 5381.
# For each character: hash = hash * 33 + ASCII value.
# Use bitwise mixing and keep the final hash within 32 bits.
# Accept a string as input and display its hash.

def custom_hash(data):
    hash_value = 5381
    for ch in data:
        hash_value ^= ((hash_value * 33) + ord(ch)) & 0xFFFFFFFF
        #bitwise mixing
        hash_value ^= (hash_value >> 16)
        hash_value ^= (hash_value * 0x45D9F3B) & 0xFFFFFFFF
    return hash_value & 0xFFFFFFFF

data = input ("Enter a string: ")
result = custom_hash(data)
print("Hash Value: ", result)
print("Hash value (hex): ", hex(result))

"""
SAMPLE I/O:
Enter a string: Hello
Hash Value:  1038428834
Hash value (hex):  0x3de52aa2
"""