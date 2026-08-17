"""
Lab 3 - Question 2: ECC (Elliptic Curve Cryptography) Encryption/Decryption
--------------------------------------------------------------------
Using ECC, encrypt the message "Secure Transactions" with the public
key. Then decrypt the ciphertext with the private key to verify the
original message.
--------------------------------------------------------------------
NOTE: Pure ECC does not directly encrypt arbitrary messages the way
RSA does -- it is fundamentally a key-agreement primitive (ECDH).
To actually "encrypt a message with ECC", the standard real-world
approach is ECIES (Elliptic Curve Integrated Encryption Scheme):

    1. The receiver (Bob) has a long-term ECC key pair.
    2. The sender (Alice) generates a one-time (ephemeral) ECC key pair.
    3. Alice and Bob each run ECDH to arrive at the SAME shared secret.
    4. The shared secret is passed through a KDF to derive an AES key.
    5. The message is actually encrypted with AES-GCM using that key.

Library used: `cryptography` (hazmat.primitives.asymmetric.ec, hkdf, aesgcm)
Curve used  : SECP256R1 (a.k.a. secp256r1 / P-256)
"""

import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_ecc_keypair():
    """Generate an ECC key pair on the SECP256R1 curve."""
    private_key = ec.generate_private_key(ec.SECP256R1())
    return private_key, private_key.public_key()


def derive_shared_key(private_key, peer_public_key) -> bytes:
    """Run ECDH and derive a 256-bit AES key from the resulting shared secret."""
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
    return HKDF(
        algorithm=hashes.SHA256(), length=32, salt=None, info=b"ecies-aes-key"
    ).derive(shared_secret)


def ecc_encrypt(message: str, receiver_public_key):
    """
    Encrypt `message` for the holder of `receiver_public_key` using ECIES.
    Returns (ephemeral_public_key_bytes, nonce, ciphertext) -- all of which
    are safe to send over an insecure channel.
    """
    ephemeral_private, ephemeral_public = generate_ecc_keypair()
    aes_key = derive_shared_key(ephemeral_private, receiver_public_key)

    nonce = os.urandom(12)
    ciphertext = AESGCM(aes_key).encrypt(nonce, message.encode("utf-8"), None)

    ephemeral_public_bytes = ephemeral_public.public_bytes(
        serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint
    )
    return ephemeral_public_bytes, nonce, ciphertext


def ecc_decrypt(ephemeral_public_bytes, nonce, ciphertext, receiver_private_key) -> str:
    """Decrypt an ECIES ciphertext using the receiver's private key."""
    ephemeral_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), ephemeral_public_bytes
    )
    aes_key = derive_shared_key(receiver_private_key, ephemeral_public_key)
    plaintext = AESGCM(aes_key).decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


def main():
    message = "Secure Transactions"
    print("=== ECC Encryption / Decryption (ECIES over secp256r1) ===\n")
    print(f"Original Message : {message}\n")

    # ---- Key Generation (Receiver / Bob) ----
    print("Generating ECC key pair (curve: secp256r1)...")
    receiver_private_key, receiver_public_key = generate_ecc_keypair()
    pub_bytes = receiver_public_key.public_bytes(
        serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint
    )
    print(f"Receiver Public Key : {pub_bytes.hex()}\n")

    # ---- Encryption (Sender / Alice) ----
    ephemeral_pub, nonce, ciphertext = ecc_encrypt(message, receiver_public_key)
    print(f"Ephemeral Public Key : {ephemeral_pub.hex()}")
    print(f"Nonce                : {nonce.hex()}")
    print(f"Ciphertext (hex)     : {ciphertext.hex()}\n")

    # ---- Decryption (Receiver / Bob) ----
    decrypted_message = ecc_decrypt(ephemeral_pub, nonce, ciphertext, receiver_private_key)
    print(f"Decrypted Message : {decrypted_message}")

    assert decrypted_message == message, "Decryption failed! Message mismatch."
    print("\n[SUCCESS] Decrypted message matches the original message.")


if __name__ == "__main__":
    main()

"""
=== ECC Encryption / Decryption (ECIES over secp256r1) ===

Original Message : Secure Transactions

Generating ECC key pair (curve: secp256r1)...
Receiver Public Key : 043227c1c031f5bd5d7278d1534bdc78906296d5ef35dc5f40b9541418846b0ad300d525c7d7e9ad4b4803d9f8eb2ce0ef8b02153ca416a4c612dc75916509f0e1

Ephemeral Public Key : 043fd50473b67de408af956275b4bfff613bdc676d2375d14d71de1ba20148514a41e11b6c5fb786a4b0695d81af22e5a4a6702edf585814010f36eb998427e1d4
Nonce                : 3d49973e50ffd617a3ceba87
Ciphertext (hex)     : 02c11ca48819d52f350b0ffd5bea9239201e68f90952cdb6519633be1223ab51b84728

Decrypted Message : Secure Transactions

[SUCCESS] Decrypted message matches the original message.
"""