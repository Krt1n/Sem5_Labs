
# PKSE: Create 10 documents, use Paillier encryption/decryption,
# build an encrypted inverted index, search and display documents.

from phe import paillier
import hashlib

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

public_key, private_key = paillier.generate_paillier_keypair()

def encrypt(data):
    return public_key.encrypt(data)

def decrypt(data):
    return private_key.decrypt(data)

def token(word):
    return hashlib.sha256(word.lower().encode()).hexdigest()

index = {}

for number, (doc_id, text) in enumerate(documents.items(), 1):
    for word in text.split():
        t = token(word)
        if t not in index:
            index[t] = []
        if number not in index[t]:
            index[t].append(number)

encrypted_index = {
    t: [encrypt(doc_num) for doc_num in ids]
    for t, ids in index.items()
}

query = input("Enter search word: ").lower()
results = encrypted_index.get(token(query), [])
ids = [decrypt(x) for x in results]

print("Matched Document IDs:",
      ["doc" + str(i) for i in ids])

for i in ids:
    doc_id = "doc" + str(i)
    print(doc_id + ":", documents[doc_id])

"""
Enter search word: cryptography 
Matched Document IDs: ['doc1', 'doc3']
doc1: information security and cryptography principles
doc3: public key cryptography uses asymmetric keys
"""