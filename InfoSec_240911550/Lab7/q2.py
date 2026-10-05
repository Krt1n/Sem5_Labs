import random


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd_val, x, y = extended_gcd(b % a, a)
        return gcd_val, y - (b // a) * x, x


def mod_inverse(e, m):
    gcd_val, x, y = extended_gcd(e, m)
    if gcd_val != 1:
        raise ValueError("Modular inverse does not exist")
    return x % m


def is_prime(n, k=5):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits=256):
    while True:
        p = random.getrandbits(bits)
        if p | 1 and is_prime(p):
            return p


class RSA:
    def __init__(self, bit_length=256):
        # Step 1: Generate two large distinct primes p and q
        p = generate_prime(bit_length)
        q = generate_prime(bit_length)
        while p == q:
            q = generate_prime(bit_length)

        self.n = p * q
        phi = (p - 1) * (q - 1)

        # Step 2: Choose public exponent e (commonly 65537)
        self.e = 65537
        while gcd(self.e, phi) != 1:
            self.e = random.randrange(3, phi, 2)

        # Step 3: Compute private exponent d
        self.d = mod_inverse(self.e, phi)

    def encrypt(self, m):
        if not (0 <= m < self.n):
            raise ValueError("Message must be in the range [0, n-1]")
        # c = m^e mod n
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        # m = c^d mod n
        return pow(c, self.d, self.n)

    def multiply_ciphertexts(self, c1, c2):
        # Multiplicative homomorphism: (c1 * c2) mod n corresponds to multiplication of plaintexts
        return (c1 * c2) % self.n


# --- Execution & Verification ---
if __name__ == "__main__":
    # Initialize RSA cryptosystem
    rsa = RSA(bit_length=256)

    # Integers to encrypt
    m1 = int(input("Enter first message: "))
    m2 = int(input("Enter second message: "))

    print(f"Original Integers: m1 = {m1}, m2 = {m2}")

    # Encrypt the integers
    c1 = rsa.encrypt(m1)
    c2 = rsa.encrypt(m2)

    print("\n--- Ciphertexts ---")
    print(f"Ciphertext 1 (c1): {c1}")
    print(f"Ciphertext 2 (c2): {c2}")

    # Perform homomorphic multiplication (c1 * c2 mod n)
    c_product = rsa.multiply_ciphertexts(c1, c2)
    print(f"\nEncrypted Product Result (c_product): {c_product}")

    # Decrypt the result of the multiplication
    decrypted_product = rsa.decrypt(c_product)
    print(f"\nDecrypted Product: {decrypted_product}")
    print(f"Expected Product: {m1 * m2}")
    print(f"Verification Successful: {decrypted_product == (m1 * m2)}")
"""
Enter first message: 3  
Enter second message: 7
Original Integers: m1 = 3, m2 = 7

--- Ciphertexts ---
Ciphertext 1 (c1): 194392749572362179276049742140951822404874907932411640951637109419353602774921316776191711929874000649997016953133149632744845649295360358011829085238286
Ciphertext 2 (c2): 311385857988472505495573634605283369982166944948765160189249426399857870386088351965731526384828420590780476991159089137098958368152463499277591675450353

Encrypted Product Result (c_product): 244907512954972834233970096200588443338065731617870008986991404528791212784139633124428284002786843330720009031172766173163397352205032441423850656387371

Decrypted Product: 21
Expected Product: 21
Verification Successful: True
"""