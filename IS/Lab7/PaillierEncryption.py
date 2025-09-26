import random
import math


def is_prime(n, k=10):
    if n < 2:
        return False
    for _ in range(k):
        a = random.randrange(2, n)
        if pow(a, n - 1, n) != 1:
            return False
    return True


def generate_prime(bits):
    while True:
        n = random.getrandbits(bits) | 1
        if is_prime(n):
            return n


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def l_function(x, n):
    return (x - 1) // n


class Paillier:
    def __init__(self, bit_length=512):
        self.p = generate_prime(bit_length // 2)
        self.q = generate_prime(bit_length // 2)
        while self.p == self.q:
            self.q = generate_prime(bit_length // 2)
        self.n = self.p * self.q
        self.n_square = self.n * self.n
        self.lambda_ = lcm(self.p - 1, self.q - 1)
        self.g = self.n + 1
        self.mu = pow(l_function(pow(self.g, self.lambda_, self.n_square), self.n), -1, self.n)

    def encrypt(self, m):
        if m >= self.n:
            raise ValueError("Message must be less than n")
        while True:
            r = random.randrange(1, self.n)
            if math.gcd(r, self.n) == 1:
                break
        return (pow(self.g, m, self.n_square) * pow(r, self.n, self.n_square)) % self.n_square

    def decrypt(self, c):
        return (l_function(pow(c, self.lambda_, self.n_square), self.n) * self.mu) % self.n

    def add(self, c1, c2):
        return (c1 * c2) % self.n_square


paillier = Paillier()
m1 = 15
m2 = 25
c1 = paillier.encrypt(m1)
c2 = paillier.encrypt(m2)
print(f"Original integers: {m1}, {m2}")
print(f"Ciphertext of {m1}: {c1}")
print(f"Ciphertext of {m2}: {c2}")
c_sum = paillier.add(c1, c2)
print(f"Encrypted sum: {c_sum}")
decrypted_sum = paillier.decrypt(c_sum)
print(f"Decrypted sum: {decrypted_sum}")
expected_sum = m1 + m2
print(f"Expected sum: {expected_sum}")
print(f"Verification: {'Correct' if decrypted_sum == expected_sum else 'Incorrect'}")
