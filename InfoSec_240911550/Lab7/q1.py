import random


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


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


class Paillier:
    def __init__(self, bit_length=256):
        # Step 1: Generate two large distinct primes p and q
        p = generate_prime(bit_length)
        q = generate_prime(bit_length)
        while p == q:
            q = generate_prime(bit_length)

        self.n = p * q
        self.n_sq = self.n * self.n
        self.lmbda = lcm(p - 1, q - 1)

        # Step 2: Select generator g (g = n + 1 is a standard choice)
        self.g = self.n + 1

        # Step 3: Compute mu = (L(g^lmbda mod n^2))^(-1) mod n
        u = pow(self.g, self.lmbda, self.n_sq)
        L = (u - 1) // self.n
        self.mu = mod_inverse(L, self.n)

    def encrypt(self, m):
        if not (0 <= m < self.n):
            raise ValueError("Message must be in the range [0, n-1]")
        # Choose a random r in Z*_n
        r = random.randrange(1, self.n)
        while gcd(r, self.n) != 1:
            r = random.randrange(1, self.n)

        # c = g^m * r^n mod n^2
        c = (pow(self.g, m, self.n_sq) * pow(r, self.n, self.n_sq)) % self.n_sq
        return c

    def decrypt(self, c):
        # m = L(c^lmbda mod n^2) * mu mod n
        u = pow(c, self.lmbda, self.n_sq)
        L = (u - 1) // self.n
        m = (L * self.mu) % self.n
        return m

    def add_ciphertexts(self, c1, c2):
        # Homomorphic addition: multiplication of ciphertexts corresponds to addition of plaintexts
        return (c1 * c2) % self.n_sq


# --- Execution & Verification ---
if __name__ == "__main__":
    # Initialize Paillier cryptosystem
    paillier = Paillier(bit_length=256)

    # Integers to encrypt
    m1 = int(input("Enter first message: "))
    m2 = int(input("Enter second message: "))

    print(f"Original Integers: m1 = {m1}, m2 = {m2}")

    # Encrypt the integers
    c1 = paillier.encrypt(m1)
    c2 = paillier.encrypt(m2)

    print("\n--- Ciphertexts ---")
    print(f"Ciphertext 1 (c1): {c1}")
    print(f"Ciphertext 2 (c2): {c2}")

    # Perform homomorphic addition (c1 * c2 mod n^2)
    c_sum = paillier.add_ciphertexts(c1, c2)
    print(f"\nEncrypted Sum Result (c_sum): {c_sum}")

    # Decrypt the result of the addition
    decrypted_sum = paillier.decrypt(c_sum)
    print(f"\nDecrypted Sum: {decrypted_sum}")
    print(f"Expected Sum: {m1 + m2}")
    print(f"Verification Successful: {decrypted_sum == (m1 + m2)}")
"""
Enter first message: 3
Enter second message: 7
Original Integers: m1 = 3, m2 = 7

--- Ciphertexts ---
Ciphertext 1 (c1): 8456529648578217389706512102298788501016613147538052707486322935876368103063599622073510855027129563222030752001965223669506544340647445569136248645847304140092229531274827454110251738349597909689280650116762570042348226931245589074314078037059147854279823447584658629187691364342293238629513258443759299365
Ciphertext 2 (c2): 4078892311997224968155388725944400759932569661904647346863440831106561583751693242060424142737618080102673851567085931569994744431630368605585481117182247180970126116012568171940859026373704734428289156379588394183939669540483460179835816615606710173221856015525290777234885991029694351345493506544572612658

Encrypted Sum Result (c_sum): 6006539976701141039522917546631490109931966672679449523015142443681976475038550541145618191447156871049327113052015531560681936692251258459130274486520949661643963145499049969762818087649815171193204430647210992161515919944140065812125398202817255982678891792555165022082728118839143563320307198100485877196

Decrypted Sum: 10
Expected Sum: 10
Verification Successful: True
"""