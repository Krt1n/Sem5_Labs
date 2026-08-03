def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


while True:
    print("\n===== MENU =====")
    print("1. Additive Cipher")
    print("2. Affine Cipher")
    print("3. Multiplicative Cipher")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        # Additive Cipher
        key = int(input("Enter the key value for Additive Cipher: "))
        text = input("Enter the text to be encrypted: ").upper()

        ciphertext = ""
        for t in text:
            if t.isalpha():
                new_char = chr((ord(t) - 65 + key) % 26 + 65)
                ciphertext += new_char
            else:
                ciphertext += t

        print("Encrypted text:", ciphertext)

        decrypted = ""
        for t in ciphertext:
            if t.isalpha():
                new_char = chr((ord(t) - 65 - key) % 26 + 65)
                decrypted += new_char
            else:
                decrypted += t

        print("Decrypted text:", decrypted)

    elif choice == 2:
        # Affine Cipher
        key1, key2 = map(int, input("Enter key1 and key2: ").split())

        if mod_inverse(key1, 26) is None:
            print("Invalid key1! It must be coprime with 26.")
            continue

        text = input("Enter the text to be encrypted: ").upper()

        ciphertext = ""
        for t in text:
            if t.isalpha():
                new_char = chr((((ord(t) - 65) * key1 + key2) % 26) + 65)
                ciphertext += new_char
            else:
                ciphertext += t

        print("Encrypted text:", ciphertext)

        decrypted = ""
        inv = mod_inverse(key1, 26)

        for t in ciphertext:
            if t.isalpha():
                new_char = chr(((inv * ((ord(t) - 65) - key2)) % 26) + 65)
                decrypted += new_char
            else:
                decrypted += t

        print("Decrypted text:", decrypted)

    elif choice == 3:
        # Multiplicative Cipher
        key = int(input("Enter the key value: "))

        if mod_inverse(key, 26) is None:
            print("Invalid key! It must be coprime with 26.")
            continue

        text = input("Enter the text to be encrypted: ").upper()

        ciphertext = ""
        for t in text:
            if t.isalpha():
                new_char = chr(((ord(t) - 65) * key) % 26 + 65)
                ciphertext += new_char
            else:
                ciphertext += t

        print("Encrypted text:", ciphertext)

        decrypted = ""
        inv = mod_inverse(key, 26)

        for t in ciphertext:
            if t.isalpha():
                new_char = chr(((ord(t) - 65) * inv) % 26 + 65)
                decrypted += new_char
            else:
                decrypted += t

        print("Decrypted text:", decrypted)

    elif choice == 4:
        print("Exiting program...")
        break

    else:
        print("Invalid choice! Please try again.")