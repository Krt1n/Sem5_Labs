import hashlib

p = 467
g = 2
x = 127

y = pow(g, x, p)

message = input("Enter message: ")

h = int(hashlib.sha256(message.encode()).hexdigest(), 16) % (p - 1)

k = 3

r = pow(g, k, p)
s = ((h - x * r) * pow(k, -1, p - 1)) % (p - 1)

print("\nPublic Key:", (p, g, y))
print("Private Key:", x)
print("Signature:", (r, s))

received = input("\nEnter message for verification: ")

h2 = int(hashlib.sha256(received.encode()).hexdigest(), 16) % (p - 1)

left = (pow(y, r, p) * pow(r, s, p)) % p
right = pow(g, h2, p)

if left == right:
    print("Signature verified successfully.")
else:
    print("Signature verification failed.")