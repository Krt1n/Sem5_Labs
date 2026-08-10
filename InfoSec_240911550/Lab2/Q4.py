from Crypto.Cipher import DES, DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


message = input("Enter message: ")
key_input = input("Enter 3DES key (48 hexadecimal characters): ")


try:
    key = bytes.fromhex(key_input)

    if len(key) != 24:
        print("Error: Key must be 48 hexadecimal characters.")

    else:
        # Generate random IV
        iv = get_random_bytes(8)

        # Check if K1 = K2 = K3
        if key[:8] == key[8:16] == key[16:24]:

            # Given key becomes single DES
            cipher = DES.new(key[:8], DES.MODE_CBC, iv)

            ciphertext = cipher.encrypt(
                pad(message.encode(), DES.block_size)
            )

            # Decryption
            cipher = DES.new(key[:8], DES.MODE_CBC, iv)

            decrypted = unpad(
                cipher.decrypt(ciphertext),
                DES.block_size
            ).decode()

        else:

            # Normal Triple DES
            key = DES3.adjust_key_parity(key)

            # Encryption
            cipher = DES3.new(key, DES3.MODE_CBC, iv)

            ciphertext = cipher.encrypt(
                pad(message.encode(), DES3.block_size)
            )

            # Decryption
            cipher = DES3.new(key, DES3.MODE_CBC, iv)

            decrypted = unpad(
                cipher.decrypt(ciphertext),
                DES3.block_size
            ).decode()


        # Output
        print("\nOriginal Message :", message)
        print("Key              :", key_input)
        print("IV               :", iv.hex().upper())
        print("Ciphertext       :", ciphertext.hex().upper())
        print("Decrypted Message:", decrypted)

        if message == decrypted:
            print("Verification     : Successful")
        else:
            print("Verification     : Failed")


except ValueError as e:
    print("Error:", e)

"""
OUTPUT:

Enter message: Classified Text
Enter 3DES key (48 hexadecimal characters): 1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF

Original Message : Classified Text
Key              : 1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF
IV               : B244EFE97FDA7F94
Ciphertext       : 954AD26826AAEB5CF80112986F822A86
Decrypted Message: Classified Text
Verification     : Successful
"""