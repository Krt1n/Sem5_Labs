"""
Lab 3 - Question 4 (Simplified): Secure File Transfer using RSA and ECC
--------------------------------------------------------------------
Design a secure file transfer system using RSA (2048-bit) and ECC
(secp256r1) to encrypt/decrypt files of different sizes, and compare
key generation, encryption, and decryption times.

WHY HYBRID ENCRYPTION?
RSA can only encrypt small messages (a few hundred bytes), and ECC
cannot encrypt messages directly at all. So for real files we:
  1. Encrypt the FILE with a fast symmetric cipher (AES).
  2. Encrypt only the small AES KEY using RSA or ECC.
This is how real-world systems (TLS, PGP, etc.) do it.
"""

import os
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def aes_encrypt(data, key):
    nonce = os.urandom(12)
    return nonce, AESGCM(key).encrypt(nonce, data, None)


def aes_decrypt(nonce, ciphertext, key):
    return AESGCM(key).decrypt(nonce, ciphertext, None)


# ---------- RSA hybrid encryption ----------
def rsa_encrypt_file(data, rsa_public_key):
    aes_key = os.urandom(32)
    nonce, ciphertext = aes_encrypt(data, aes_key)
    wrapped_key = PKCS1_OAEP.new(rsa_public_key).encrypt(aes_key)
    return wrapped_key, nonce, ciphertext


def rsa_decrypt_file(wrapped_key, nonce, ciphertext, rsa_private_key):
    aes_key = PKCS1_OAEP.new(rsa_private_key).decrypt(wrapped_key)
    return aes_decrypt(nonce, ciphertext, aes_key)


# ---------- ECC hybrid encryption (ECIES) ----------
def ecc_encrypt_file(data, ecc_public_key):
    ephemeral_private = ec.generate_private_key(ec.SECP256R1())
    shared_secret = ephemeral_private.exchange(ec.ECDH(), ecc_public_key)
    aes_key = HKDF(hashes.SHA256(), 32, None, b"file-transfer").derive(shared_secret)

    nonce, ciphertext = aes_encrypt(data, aes_key)
    ephemeral_public_bytes = ephemeral_private.public_key().public_bytes(
        serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
    return ephemeral_public_bytes, nonce, ciphertext


def ecc_decrypt_file(ephemeral_public_bytes, nonce, ciphertext, ecc_private_key):
    ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), ephemeral_public_bytes)
    shared_secret = ecc_private_key.exchange(ec.ECDH(), ephemeral_public_key)
    aes_key = HKDF(hashes.SHA256(), 32, None, b"file-transfer").derive(shared_secret)
    return aes_decrypt(nonce, ciphertext, aes_key)


def main():
    print("=== Secure File Transfer: RSA-2048 vs ECC (secp256r1) ===\n")

    # ---- Key generation ----
    t0 = time.perf_counter()
    rsa_private_key = RSA.generate(2048)
    rsa_public_key = rsa_private_key.publickey()
    rsa_keygen_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    ecc_private_key = ec.generate_private_key(ec.SECP256R1())
    ecc_public_key = ecc_private_key.public_key()
    ecc_keygen_time = time.perf_counter() - t0

    print(f"RSA key generation time : {rsa_keygen_time:.4f} s")
    print(f"ECC key generation time : {ecc_keygen_time:.4f} s\n")

    # ---- Encrypt/decrypt files of different sizes ----
    for size_mb in [1, 10]:
        file_data = os.urandom(size_mb * 1024 * 1024)  # simulated file

        t0 = time.perf_counter()
        wrapped_key, nonce, ciphertext = rsa_encrypt_file(file_data, rsa_public_key)
        rsa_enc_time = time.perf_counter() - t0

        t0 = time.perf_counter()
        rsa_decrypted = rsa_decrypt_file(wrapped_key, nonce, ciphertext, rsa_private_key)
        rsa_dec_time = time.perf_counter() - t0
        assert rsa_decrypted == file_data

        t0 = time.perf_counter()
        eph_pub, e_nonce, e_ciphertext = ecc_encrypt_file(file_data, ecc_public_key)
        ecc_enc_time = time.perf_counter() - t0

        t0 = time.perf_counter()
        ecc_decrypted = ecc_decrypt_file(eph_pub, e_nonce, e_ciphertext, ecc_private_key)
        ecc_dec_time = time.perf_counter() - t0
        assert ecc_decrypted == file_data

        print(f"File size: {size_mb} MB")
        print(f"  RSA -> encrypt: {rsa_enc_time:.4f}s | decrypt: {rsa_dec_time:.4f}s")
        print(f"  ECC -> encrypt: {ecc_enc_time:.4f}s | decrypt: {ecc_dec_time:.4f}s\n")

    print("[SUCCESS] All files encrypted and decrypted correctly with both RSA and ECC.")
    print("\nObservation: RSA key generation is much slower than ECC. File encryption/")
    print("decryption speed is nearly the same for both, since the actual file is")
    print("always encrypted with AES -- RSA/ECC only protect the small AES key.")


if __name__ == "__main__":
    main()

"""
=== Secure File Transfer: RSA-2048 vs ECC (secp256r1) ===

RSA key generation time : 0.0822 s
ECC key generation time : 0.0005 s

File size: 1 MB
  RSA -> encrypt: 0.0024s | decrypt: 0.0015s
  ECC -> encrypt: 0.0007s | decrypt: 0.0004s

File size: 10 MB
  RSA -> encrypt: 0.0032s | decrypt: 0.0033s
  ECC -> encrypt: 0.0027s | decrypt: 0.0034s

[SUCCESS] All files encrypted and decrypted correctly with both RSA and ECC.

Observation: RSA key generation is much slower than ECC. File encryption/
decryption speed is nearly the same for both, since the actual file is
always encrypted with AES -- RSA/ECC only protect the small AES key.
"""