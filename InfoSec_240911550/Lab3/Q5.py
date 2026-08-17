"""
Lab 3 - Question 5: Diffie-Hellman Key Exchange for P2P File Sharing
--------------------------------------------------------------------
As part of a project to enhance the security of communication in a
peer-to-peer file sharing system, implement a secure key exchange
mechanism using the Diffie-Hellman algorithm. Each peer must establish
a shared secret key with another peer over an insecure channel.
Generate public/private keys, compute the shared secret, and measure
the time taken for key generation and key exchange.
--------------------------------------------------------------------
Library used: `cryptography` (hazmat.primitives.asymmetric.dh)
"""

import time
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


class Peer:
    """A single peer in the P2P network participating in DH key exchange."""

    def __init__(self, name: str, parameters):
        self.name = name
        self.parameters = parameters
        self.private_key = None
        self.public_key = None
        self.shared_key = None

    def generate_keypair(self) -> float:
        """Generate this peer's private/public DH key pair. Returns elapsed time (s)."""
        start = time.perf_counter()
        self.private_key = self.parameters.generate_private_key()
        self.public_key = self.private_key.public_key()
        return time.perf_counter() - start

    def compute_shared_key(self, peer_public_key) -> float:
        """
        Compute the shared secret from this peer's private key and the
        other peer's PUBLIC key (which is all that ever crosses the
        insecure channel). Returns elapsed time (s).
        """
        start = time.perf_counter()
        shared_secret = self.private_key.exchange(peer_public_key)
        # Raw DH output isn't a "nice" uniform key -- pass it through a KDF.
        self.shared_key = HKDF(
            algorithm=hashes.SHA256(), length=32, salt=None, info=b"p2p-dh-exchange"
        ).derive(shared_secret)
        return time.perf_counter() - start


def main():
    print("=== Diffie-Hellman Key Exchange: Peer-to-Peer File Sharing ===\n")

    # ---- Shared public DH domain parameters (prime p, generator g) ----
    print("Generating shared DH domain parameters (2048-bit)...")
    t0 = time.perf_counter()
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    param_time = time.perf_counter() - t0
    print(f"Domain parameter generation time : {param_time:.6f} s\n")

    peer_alice = Peer("Alice", parameters)
    peer_bob = Peer("Bob", parameters)

    # ---- Each peer generates its OWN private/public key pair ----
    alice_keygen_time = peer_alice.generate_keypair()
    bob_keygen_time = peer_bob.generate_keypair()
    print(f"Alice key generation time : {alice_keygen_time:.6f} s")
    print(f"Bob key generation time   : {bob_keygen_time:.6f} s\n")

    print("Peers now exchange only their PUBLIC keys over the insecure channel.")
    print("(Private keys never leave each peer's machine.)\n")

    # ---- Each peer independently computes the SAME shared secret ----
    alice_exchange_time = peer_alice.compute_shared_key(peer_bob.public_key)
    bob_exchange_time = peer_bob.compute_shared_key(peer_alice.public_key)
    print(f"Alice shared-key computation time : {alice_exchange_time:.6f} s")
    print(f"Bob shared-key computation time   : {bob_exchange_time:.6f} s\n")

    print(f"Alice's derived shared key : {peer_alice.shared_key.hex()}")
    print(f"Bob's derived shared key   : {peer_bob.shared_key.hex()}")

    assert peer_alice.shared_key == peer_bob.shared_key, "Shared keys do not match!"
    print("\n[SUCCESS] Alice and Bob independently derived the SAME shared secret key")
    print("without ever transmitting it. This key can now be used as an AES key")
    print("to encrypt files exchanged directly between the two peers.")

    print("\n=== Timing Summary ===")
    print(f"{'Step':<35}{'Time (s)':<10}")
    print(f"{'Domain parameter generation':<35}{param_time:<10.6f}")
    print(f"{'Alice key pair generation':<35}{alice_keygen_time:<10.6f}")
    print(f"{'Bob key pair generation':<35}{bob_keygen_time:<10.6f}")
    print(f"{'Alice shared secret computation':<35}{alice_exchange_time:<10.6f}")
    print(f"{'Bob shared secret computation':<35}{bob_exchange_time:<10.6f}")


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