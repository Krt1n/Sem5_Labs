
# SSE: Create 10 documents, use AES encryption/decryption,
# build an encrypted inverted index, search and display documents.

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import hmac

documents = {
    "doc1": "information security and cryptography principles",
    "doc2": "symmetric searchable encryption protects privacy",
    "doc3": "public key cryptography uses asymmetric keys",
    "doc4": "data confidentiality and searchability are essential",
    "doc5": "advanced encryption standard secures data blocks",
    "doc6": "inverted index maps words to document identifiers",
    "doc7": "hash functions provide integrity and secure hashing",
    "doc8": "search query is encrypted before matching terms",
    "doc9": "cryptographic primitives ensure secure data storage",
    "doc10": "network security and intrusion detection systems"
}

key = get_random_bytes(16)
token_key = get_random_bytes(32)

def encrypt(data):
    cipher = AES.new(key, AES.MODE_CBC)
    return cipher.iv + cipher.encrypt(pad(data.encode(), 16))

def decrypt(data):
    cipher = AES.new(key, AES.MODE_CBC, data[:16])
    return unpad(cipher.decrypt(data[16:]), 16).decode()

def token(word):
    return hmac.new(token_key, word.lower().encode(),
                    hashlib.sha256).digest()

index = {}

for doc_id, text in documents.items():
    for word in text.split():
        t = token(word)
        if t not in index:
            index[t] = []
        if doc_id not in index[t]:
            index[t].append(doc_id)

encrypted_index = {
    t: [encrypt(doc_id) for doc_id in ids]
    for t, ids in index.items()
}

query = input("Enter search word: ").lower()
results = encrypted_index.get(token(query), [])
ids = [decrypt(x) for x in results]

print("Matched Document IDs:", ids)
for doc_id in ids:
    print(doc_id + ":", documents[doc_id])
"""
Enter search word: encryption
Matched Document IDs: ['doc2', 'doc5']
doc2: symmetric searchable encryption protects privacy
doc5: advanced encryption standard secures data blocks
"""