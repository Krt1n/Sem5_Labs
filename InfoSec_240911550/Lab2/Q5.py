from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes


# -----------------------------
# Input
# -----------------------------

message = input("Enter message: ")
key_input = input("Enter AES-192 key (48 hexadecimal characters): ")


try:
    # Convert hexadecimal key to bytes
    key = bytes.fromhex(key_input)

    # AES-192 requires 24 bytes
    if len(key) != 24:
        print("\nError: AES-192 requires a 24-byte key.")
        print("You entered", len(key), "bytes.")
        print("AES-192 key must contain 48 hexadecimal characters.")

    else:

        # -----------------------------
        # Key Expansion
        # -----------------------------
        #
        # PyCryptodome performs AES key
        # expansion internally.

        print("\n========== AES-192 ENCRYPTION ==========")

        print("\nOriginal Message:")
        print(message)

        print("\nOriginal Key:")
        print(key_input)

        print("\nKey Length:")
        print(len(key) * 8, "bits")

        # -----------------------------
        # Initial Round
        # -----------------------------

        iv = get_random_bytes(16)

        cipher = AES.new(key, AES.MODE_CBC, iv)

        padded_message = pad(
            message.encode(),
            AES.block_size
        )

        print("\nIV:")
        print(iv.hex().upper())

        print("\nPadded Message:")
        print(padded_message.hex().upper())

        # -----------------------------
        # Encryption
        # -----------------------------

        ciphertext = cipher.encrypt(padded_message)

        print("\nCiphertext:")
        print(ciphertext.hex().upper())

        # -----------------------------
        # Display AES Rounds
        # -----------------------------

        print("\n========== AES ROUNDS ==========")

        print("\nKey Expansion:")
        print("AES-192 uses 12 encryption rounds.")
        print("The AES library performs key expansion internally.")

        print("\nInitial Round:")
        print("AddRoundKey")

        print("\nMain Rounds:")
        for i in range(1, 12):
            print("Round", i, ":")
            print("  SubBytes")
            print("  ShiftRows")
            print("  MixColumns")
            print("  AddRoundKey")

        print("\nFinal Round:")
        print("SubBytes")
        print("ShiftRows")
        print("AddRoundKey")
        print("(No MixColumns in final round)")

        # -----------------------------
        # Output
        # -----------------------------

        print("\n========== RESULT ==========")

        print("Message   :", message)
        print("Key       :", key_input)
        print("Ciphertext:", ciphertext.hex().upper())

except ValueError:
    print("\nError: Enter a valid hexadecimal key.")
