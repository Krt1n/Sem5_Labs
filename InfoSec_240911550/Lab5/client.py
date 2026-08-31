# Q2. Client sends data and verifies its integrity.
# Compare local hash with server's hash.

import socket
import hashlib

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

data = input("Enter your message: ")

data_bytes = data.encode()

local_hash = hashlib.sha256(data_bytes).hexdigest()

print("Client Hash:",local_hash)

client.send(data_bytes)

server_hash = client.recv(4096).decode()

print("Server Hash:",server_hash)

if local_hash == server_hash:
    print("Data Integrity: VERIFIED")
    print("No corruption or tampering detected")
else:
    print("Data Integrity: NOT VERIFIED")
    print("Data may corrupted or tampered with")

client.close()
"""
Server waiting for connection.....
Connected to: ('127.0.0.1', 50762)
Recieved Data: Hello Server
Server hash: be96b72444ca7cda0055012a1f99f418f98c25b2ee0e83d4f88c153ef696589e

Enter your message: Hello Server
Client Hash: be96b72444ca7cda0055012a1f99f418f98c25b2ee0e83d4f88c153ef696589e
Server Hash: be96b72444ca7cda0055012a1f99f418f98c25b2ee0e83d4f88c153ef696589e
Data Integrity: VERIFIED
No corruption or tampering detected
"""