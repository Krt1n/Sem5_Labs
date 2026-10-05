import socket

p = 23
g = 5

b = int(input("Enter server private key: "))

B = pow(g, b, p)

server = socket.socket()
server.bind(("localhost", 9999))
server.listen(1)

print("Waiting for client...")

conn, addr = server.accept()

conn.send(str(B).encode())

A = int(conn.recv(1024).decode())

shared_secret = pow(A, b, p)

print("Server public key:", B)
print("Client public key:", A)
print("Server shared secret:", shared_secret)

conn.send(str(shared_secret).encode())

conn.close()
server.close()







import socket

p = 23
g = 5

a = int(input("Enter client private key: "))

A = pow(g, a, p)

client = socket.socket()
client.connect(("localhost", 9999))

B = int(client.recv(1024).decode())

client.send(str(A).encode())

shared_secret = pow(B, a, p)

server_secret = int(client.recv(1024).decode())

print("Client public key:", A)
print("Server public key:", B)
print("Client shared secret:", shared_secret)

if shared_secret == server_secret:
    print("Key exchange verified successfully.")
else:
    print("Key exchange failed.")

client.close()