key = int(input("Enter the key values for Multiplicative cipher: "))
text = input("Enter the text to be encrypted: ")
ciphertext = ""
text=text.upper()

def mod_inverse(a,m):
    for x in range(1,m):
        if(a*x)%m==1:
            return x
    return None

for t in text:
    if t.isalpha():
        new_char = chr(((ord(t)-65)*key)%26 + 65)
        ciphertext += new_char
    else:
        ciphertext += t
print("Encrypted text is: " + ciphertext)

Decrypted = ""
for t in ciphertext:
    if t.isalpha():
        new_char = chr(((ord(t)-65)*mod_inverse(key,26))%26 + 65)
        Decrypted += new_char
    else:
        Decrypted += t
print("Decrypted text is: " + Decrypted)



