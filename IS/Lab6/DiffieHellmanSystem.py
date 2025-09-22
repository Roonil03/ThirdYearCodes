from Crypto.Random.random import randint

# Using small prime numbers for simplicity
P = 23  # A large prime number
G = 5   # A primitive root modulo P

# Alice generates private and public key
a_private = randint(1, P - 1)
a_public = pow(G, a_private, P)

# Bob generates private and public key
b_private = randint(1, P - 1)
b_public = pow(G, b_private, P)

# Exchange and compute shared keys
a_shared = pow(b_public, a_private, P)
b_shared = pow(a_public, b_private, P)

assert a_shared == b_shared

print("Shared secret key:", a_shared)
