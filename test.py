import random

# Publicly shared values
p = 23  # Prime number (small for demo, should be large in practice)
g = 5   # Primitive root modulo p

# Alice's private key (secret)
a = random.randint(1, p-2)
# Bob's private key (secret)
b = random.randint(1, p-2)

# Alice computes her public key
A = pow(g, a, p)
# Bob computes his public key
B = pow(g, b, p)

# Exchange public keys...

# Alice computes the shared secret
shared_secret_alice = pow(B, a, p)
# Bob computes the shared secret
shared_secret_bob = pow(A, b, p)

print("Alice's Secret:", shared_secret_alice)
print("Bob's Secret:  ", shared_secret_bob)
print("They match?    ", shared_secret_alice == shared_secret_bob)
