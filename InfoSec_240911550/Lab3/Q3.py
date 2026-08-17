"""
Lab 3 - Question 3: ElGamal Encryption/Decryption
--------------------------------------------------------------------
Given an ElGamal encryption scheme with a public key (p, g, h) and a
private key x, encrypt the message "Confidential Data". Then decrypt
the ciphertext to retrieve the original message.
--------------------------------------------------------------------
ElGamal has no ready-made "encrypt this string" function in most
libraries, so we implement the algorithm ourselves (as taught in the
manual), using PyCryptodome's Crypto.Util.number only for safe prime
generation. Each character of the message is encrypted as its own
integer block (m = ASCII value), producing a ciphertext pair (c1, c2)
per character.
"""

import random
from Crypto.Util import number


def generate_elgamal_keys(key_size: int = 256):
    """
    Generate ElGamal domain parameters and a key pair.
        p : large prime modulus
        g : generator of the multiplicative group mod p
        x : private key,        1 <= x <= p-2
        h : public key component, h = g^x mod p
    """
    p = number.getPrime(key_size)
    g = random.randint(2, p - 2)
    x = random.randint(2, p - 2)      # private key
    h = pow(g, x, p)                  # public key component
    return p, g, h, x


def elgamal_encrypt_block(m: int, p: int, g: int, h: int):
    """Encrypt a single integer block m (0 <= m < p)."""
    k = random.randint(2, p - 2)      # fresh random key for EVERY encryption
    c1 = pow(g, k, p)
    c2 = (m * pow(h, k, p)) % p
    return c1, c2


def elgamal_decrypt_block(c1: int, c2: int, p: int, x: int) -> int:
    """Decrypt a single ciphertext pair (c1, c2) using private key x."""
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)             # modular inverse of s mod p
    return (c2 * s_inv) % p


def elgamal_encrypt_message(message: str, p: int, g: int, h: int):
    """Encrypt a text message character-by-character (ASCII value = m)."""
    return [elgamal_encrypt_block(ord(ch), p, g, h) for ch in message]


def elgamal_decrypt_message(ciphertext, p: int, x: int) -> str:
    """Decrypt a list of (c1, c2) pairs back into the original text."""
    return "".join(chr(elgamal_decrypt_block(c1, c2, p, x)) for c1, c2 in ciphertext)


def main():
    message = "Confidential Data"
    print("=== ElGamal Encryption / Decryption ===\n")
    print(f"Original Message : {message}\n")

    # ---- Key Generation ----
    print("Generating ElGamal domain parameters and keys (256-bit prime)...")
    p, g, h, x = generate_elgamal_keys(256)
    print(f"Public Key (p, g, h):")
    print(f"  p = {p}")
    print(f"  g = {g}")
    print(f"  h = {h}")
    print(f"Private Key (x) = {x}\n")

    # ---- Encryption ----
    ciphertext = elgamal_encrypt_message(message, p, g, h)
    print("Ciphertext ((c1, c2) pair per character):")
    for i, (c1, c2) in enumerate(ciphertext):
        print(f"  [{i:2d}] '{message[i]}' -> (c1={c1}, c2={c2})")
    print()

    # ---- Decryption ----
    decrypted_message = elgamal_decrypt_message(ciphertext, p, x)
    print(f"Decrypted Message : {decrypted_message}")

    assert decrypted_message == message, "Decryption failed! Message mismatch."
    print("\n[SUCCESS] Decrypted message matches the original message.")


if __name__ == "__main__":
    main()

"""
Domain parameter generation time : 4.692167 s

Alice key generation time : 0.001291 s
Bob key generation time   : 0.001242 s

Peers now exchange only their PUBLIC keys over the insecure channel.
(Private keys never leave each peer's machine.)

Alice shared-key computation time : 0.001490 s
Bob shared-key computation time   : 0.001242 s

Alice's derived shared key : 3a6d5c25733127844a8902a146e73ee02dce68eb2fe258b2bbaf0e3513be5b9d
Bob's derived shared key   : 3a6d5c25733127844a8902a146e73ee02dce68eb2fe258b2bbaf0e3513be5b9d

[SUCCESS] Alice and Bob independently derived the SAME shared secret key
without ever transmitting it. This key can now be used as an AES key
to encrypt files exchanged directly between the two peers.

=== Timing Summary ===
Step                               Time (s)  
Domain parameter generation        4.692167  
Alice key pair generation          0.001291  
Bob key pair generation            0.001242  
Alice shared secret computation    0.001490  
Bob shared secret computation      0.001242  
"""