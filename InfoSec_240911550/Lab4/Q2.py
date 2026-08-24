"""
HealthCare Inc., a leading healthcare provider, has implemented a secure patient data
management system using the Rabin cryptosystem. The system allows authorized healthcare
professionals to securely access and manage patient records across multiple hospitals and
clinics within the organization. Implement a Python-based centralized key management
service that can:
• Key Generation: Generate public and private key pairs for each hospital and clinic using
the Rabin cryptosystem. The key size should be configurable (e.g., 1024 bits).
• Key Distribution: Provide a secure API for hospitals and clinics to request and receive
their public and private key pairs.
• Key Revocation: Implement a process to revoke and update the keys of a hospital or
clinic when necessary (e.g., when a facility is closed or compromised).
• Key Renewal: Automatically renew the keys of all hospitals and clinics at regular
intervals (e.g., every 12 months) to maintain the security of the patient data management
system.
• Secure Storage: Securely store the private keys of all hospitals and clinics, ensuring that
they are not accessible to unauthorized parties.
• Auditing and Logging: Maintain detailed logs of all key management operations, such
as key generation, distribution, revocation, and renewal, to enable auditing and
compliance reporting.
• Regulatory Compliance: Ensure that the key management service and its operations are
compliant with relevant data privacy regulations (e.g., HIPAA).
• Perform a trade-off analysis to compare the workings of Rabin and RSA.
"""


import secrets
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
import json

SIZE = int(input("Enter key size: "))

fer = Fernet(Fernet.generate_key())
db = {}

def prime(n):
    if n < 2:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True

def gen_prime(bits):
    while True:
        n = secrets.randbits(bits) | (1 << bits - 1) | 3
        if n % 4 == 3 and prime(n):
            return n

def gen_keys(bits):
    p = gen_prime(bits // 2)
    q = gen_prime(bits // 2)

    while p == q:
        q = gen_prime(bits // 2)

    return p * q, p, q

def audit(msg):
    with open("kms.log", "a") as f:
        f.write(f"{datetime.now()} : {msg}\n")

def add(name):
    n, p, q = gen_keys(SIZE)

    db[name] = {
        "pub": n,
        "pri": fer.encrypt(json.dumps([p, q]).encode()).decode(),
        "expiry": datetime.now() + timedelta(days=365),
        "active": True
    }

    audit("KEY GENERATED: " + name)
    print("Key generated for", name)

def distribute(name):
    if name not in db or not db[name]["active"]:
        print("Invalid or revoked facility")
        return

    k = db[name]
    pq = json.loads(fer.decrypt(k["pri"].encode()).decode())

    print("Public Key :", k["pub"])
    print("Private Key:", pq)
    print("Expiry     :", k["expiry"])

    audit("KEY DISTRIBUTED: " + name)

def revoke(name):
    if name in db:
        db[name]["active"] = False
        audit("KEY REVOKED: " + name)
        print("Key revoked")
    else:
        print("Facility not found")

def renew(name):
    if name in db:
        add(name)
        audit("KEY RENEWED: " + name)
    else:
        print("Facility not found")

def check():
    for name, k in db.items():
        if datetime.now() >= k["expiry"]:
            print(name, "-> Expired")
        else:
            print(name, "-> Active")

while True:
    print("\n1. Generate Key")
    print("2. Distribute Key")
    print("3. Revoke Key")
    print("4. Renew Key")
    print("5. Check Keys")
    print("6. Exit")

    ch = input("Enter choice: ")

    if ch == "1":
        add(input("Enter hospital/clinic: "))

    elif ch == "2":
        distribute(input("Enter hospital/clinic: "))

    elif ch == "3":
        revoke(input("Enter hospital/clinic: "))

    elif ch == "4":
        renew(input("Enter hospital/clinic: "))

    elif ch == "5":
        check()

    elif ch == "6":
        break

    else:
        print("Invalid choice")

"""
Enter key size: 16

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 1
Enter hospital/clinic: HospitalA
Key generated for HospitalA

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 1
Enter hospital/clinic: ClincA
Key generated for ClincA

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 5
HospitalA -> Active
ClincA -> Active

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 2
Enter hospital/clinic: HospitalA
Public Key : 29737
Private Key: [131, 227]
Expiry     : 2027-08-24 15:55:17.263285

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 3
Enter hospital/clinic: HospitalA
Key revoked

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 5
HospitalA -> Active
ClincA -> Active

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 2
Enter hospital/clinic: HospitalA
Invalid or revoked facility

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 4
Enter hospital/clinic: ClincA
Key generated for ClinicA

1. Generate Key
2. Distribute Key
3. Revoke Key
4. Renew Key
5. Check Keys
6. Exit
Enter choice: 6
"""
