# Q2. Use Python sockets to verify data integrity.
# Client sends data to server.
# Server computes its hash and sends the hash back.
# Client computes its own hash and compares both hashes.
# Demonstrate detection of corrupted/tampered data.

import socket
import hashlib

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(1)

print("Server waiting for connection.....")

conn, addr = server.accept()
print("Connected to:", addr)

data = conn.recv(4096)

print("Recieved Data:", data.decode())

server_hash = hashlib.sha256(data).hexdigest()

print("Server hash:", server_hash)

conn.send(server_hash.encode())

conn.close()
server.close()
"""
Server waiting for connection.....
Connected to: ('127.0.0.1', 56542)
Recieved Data: Hello Server
Server hash: be96b72444ca7cda0055012a1f99f418f98c25b2ee0e83d4f88c153ef696589e
"""