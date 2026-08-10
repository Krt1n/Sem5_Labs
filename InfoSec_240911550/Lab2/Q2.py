"""Encrypt the message "Sensitive Information" using AES-128 with the following key:
"0123456789ABCDEF0123456789ABCDEF". Then decrypt the ciphertext to verify the
original message."""

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Encryption
def encrypt(message, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return iv, encrypted

# Decryption
def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(ciphertext),AES.block_size)
    return decrypted.decode()

# Main Program
message = input("Enter message: ")
key_input = input("Enter AES-128 key (32 hexadecimal characters): ")

# Check key length
if len(key_input) != 32:
    print("Error: AES-128 key must be exactly 32 hexadecimal characters.")

else:
    try:
        # Convert hexadecimal key to bytes
        key = bytes.fromhex(key_input)
        # Check that it is exactly 16 bytes
        if len(key) != 16:
            print("Error: AES-128 key must be 16 bytes.")
        else:
            # Encrypt
            iv, ciphertext = encrypt(message, key)
            # Convert to hexadecimal for display
            iv_hex = iv.hex().upper()
            ciphertext_hex = ciphertext.hex().upper()
            # Decrypt
            decrypted = decrypt(ciphertext, key, iv)
            # Display results
            print()
            print("Original Message :", message)
            print("Key              :", key_input)
            print("IV               :", iv_hex)
            print("Ciphertext       :", ciphertext_hex)
            print("Decrypted        :", decrypted)
            # Verification
            if message == decrypted:
                print("Verification     : Successful")
            else:
                print("Verification     : Failed")

    except ValueError:
        print("Error: Key must contain only hexadecimal characters (0-9, A-F).")

"""
OUTPUT:

Enter message: Sensitive Information
Enter AES-128 key (32 hexadecimal characters): 0123456789ABCDEF0123456789ABCDEF

Original Message : Sensitive Information
Key              : 0123456789ABCDEF0123456789ABCDEF
IV               : 689A6FA37B8217454FE20CEC0230F757
Ciphertext       : 0A924AE551938843F9B4FECD72ADDF0C242BFFE4B680C02587E8D7952735B614
Decrypted        : Sensitive Information
Verification     : Successful
"""