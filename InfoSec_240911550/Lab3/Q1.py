"""
Lab 3 - Question 1: RSA Encryption/Decryption
--------------------------------------------------------------------
Using RSA, encrypt the message "Asymmetric Encryption" with the
public key (n, e). Then decrypt the ciphertext with the private
key (n, d) to verify the original message.
--------------------------------------------------------------------
Library used : PyCryptodome (Crypto.PublicKey.RSA, Crypto.Cipher.PKCS1_OAEP)
"""

import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def generate_rsa_keys(key_size: int = 2048):
    """Generate an RSA private/public key pair."""
    private_key = RSA.generate(key_size)
    public_key = private_key.publickey()
    return private_key, public_key


def rsa_encrypt(message: str, public_key) -> bytes:
    """Encrypt a UTF-8 string using the RSA public key (OAEP padding)."""
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message.encode("utf-8"))


def rsa_decrypt(ciphertext: bytes, private_key) -> str:
    """Decrypt ciphertext bytes using the RSA private key (OAEP padding)."""
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext).decode("utf-8")


def main():
    message = "Asymmetric Encryption"
    print("=== RSA Encryption / Decryption ===\n")
    print(f"Original Message : {message}\n")

    # ---- Key Generation ----
    print("Generating RSA key pair (2048-bit)...")
    private_key, public_key = generate_rsa_keys(2048)
    print(f"Public Key  -> n : {public_key.n.bit_length()}-bit modulus, e = {public_key.e}")
    print(f"Private Key -> d : {private_key.d.bit_length()}-bit exponent\n")

    # ---- Encryption using public key (n, e) ----
    ciphertext = rsa_encrypt(message, public_key)
    print(f"Ciphertext (hex) : {binascii.hexlify(ciphertext).decode()}\n")

    # ---- Decryption using private key (n, d) ----
    decrypted_message = rsa_decrypt(ciphertext, private_key)
    print(f"Decrypted Message : {decrypted_message}")

    # ---- Verification ----
    assert decrypted_message == message, "Decryption failed! Message mismatch."
    print("\n[SUCCESS] Decrypted message matches the original message.")


if __name__ == "__main__":
    main()

"""
=== RSA Encryption / Decryption ===

Original Message : Asymmetric Encryption

Generating RSA key pair (2048-bit)...
Public Key  -> n : 2048-bit modulus, e = 65537
Private Key -> d : 2044-bit exponent

Ciphertext (hex) : 81e15095893f0bbc178decad408503ca9216243d3517437d3c312ec8aa334c7be6612bf7f31b7934e0ebd53f53a0a287ee0c9631c8e0910e1d1fb610bcfb86c264f60fb8200d256a458eeb17f223d4ebb614c08fb3e939fd09c2254a8e010d2e47e69099357030bd539993dd268ef6647a810e4c848643609f7f0ede53aa7f32c8c88b0ea4d1afc746b2aee4fd3bacb0f84ae1f2f5d77c4ecc08c7e8612551b15ebd4217b81edf88183574efafa72e18aacec2d90d97e2249e3fb99c84b28428cfdcd84d2635d24d229b7c32d4540e3730139b02d53c01ee1ddfbabfbb682a8c232b1435240746488b9c4f96e785f34da8cb56b33bb2033054e1967027ac795e

Decrypted Message : Asymmetric Encryption

[SUCCESS] Decrypted message matches the original message.
"""