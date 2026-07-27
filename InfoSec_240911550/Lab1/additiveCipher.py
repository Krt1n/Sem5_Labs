key = int(input("Enter the key values for Additive cipher: "))
text = input("Enter the text to be encrypted: ")
ciphertext = ""
text=text.upper()
for t in text:
    new_char = chr((ord(t)-65+key)%26 + 65)
    ciphertext += new_char
print("Encrypted text is: " + ciphertext)

Decrypted = ""
for t in ciphertext:
    new_char = chr((ord(t)-65-key)%26 + 65)
    Decrypted += new_char
print("Decrypted text is: " + Decrypted)



