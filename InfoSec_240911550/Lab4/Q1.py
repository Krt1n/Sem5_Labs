"""
 Q1 — Short Version

**SecureCorp** has three systems: **Finance, HR, and Supply Chain** that need to securely exchange sensitive documents.

Develop a **Python program** that:

1. Uses **RSA encryption** and **Diffie-Hellman key exchange** for secure communication.
2. Provides **key management** for generating, distributing, and revoking keys.
3. Supports **scalability**, allowing new systems to be added easily.

"""

import math
import secrets

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def inv(a, m):
    return pow(a, -1, m)

def rsa_keys(p, q):
    n = p * q
    ph = (p - 1) * (q - 1)
    e = 65537
    if math.gcd(e, ph) != 1:
        e = 3
    d = inv(e, ph)
    return (n, e), (n, d)

def rsa_enc(m, pub):
    n, e = pub
    return pow(m, e, n)

def rsa_dec(c, pri):
    n, d = pri
    return pow(c, d, n)

class KMS:
    def __init__(self):
        self.keys = {}

    def add(self, name, pub, pri):
        self.keys[name] = {"pub": pub, "pri": pri, "active": True}

    def revoke(self, name):
        if name in self.keys:
            self.keys[name]["active"] = False

    def show(self):
        for name, k in self.keys.items():
            print(name, "->", "Active" if k["active"] else "Revoked")

# RSA setup
p, q = 61, 53
pub, pri = rsa_keys(p, q)

kms = KMS()
kms.add("Finance", pub, pri)
kms.add("HR", pub, pri)
kms.add("SupplyChain", pub, pri)

print("Key Management System")
kms.show()

name = input("\nEnter system to revoke: ")
if name in kms.keys:
    kms.revoke(name)

kms.show()

# RSA communication
m = int(input("\nEnter plaintext number (< n): "))
c = rsa_enc(m, pub)
print("RSA Ciphertext:", c)
print("RSA Decrypted:", rsa_dec(c, pri))

# Diffie-Hellman
p = 23
g = 5

a = secrets.randbelow(p - 2) + 1
b = secrets.randbelow(p - 2) + 1

A = pow(g, a, p)
B = pow(g, b, p)

ka = pow(B, a, p)
kb = pow(A, b, p)

print("\nDiffie-Hellman")
print("Alice Public Key:", A)
print("Bob Public Key:", B)
print("Shared Key:", ka)

if ka == kb:
    print("Secure shared key established")

"""
Key Management System
Finance -> Active
HR -> Active
SupplyChain -> Active

Enter system to revoke: Finance
Finance -> Revoked
HR -> Active
SupplyChain -> Active

Enter plaintext number (< n): 65
RSA Ciphertext: 2790
RSA Decrypted: 65

Diffie-Hellman
Alice Public Key: 16
Bob Public Key: 15
Shared Key: 4
Secure shared key established
"""
