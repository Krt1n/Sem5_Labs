key1,key2= map(int,input("Enter the key values for Affine cipher: ").split())
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
        new_char = chr((((ord(t)-65)*key1)+key2)%26 + 65)
        ciphertext += new_char
    else:
        ciphertext += t
print("Encrypted text is: " + ciphertext)

Decrypted = ""
for t in ciphertext:
    if t.isalpha():
        new_char = chr((mod_inverse(key1,26)*(ord(t)-65)-(mod_inverse(key1,26)*key2))%26 + 65)
        Decrypted += new_char
    else:
        Decrypted += t
print("Decrypted text is: " + Decrypted)



