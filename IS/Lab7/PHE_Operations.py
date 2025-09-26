import random
import math
import timeit

class Paillier:
    def __init__(self, bit_length=256):  # Smaller for demo
        self.p = self.generate_prime(bit_length // 2)
        self.q = self.generate_prime(bit_length // 2)
        while self.p == self.q:
            self.q = self.generate_prime(bit_length // 2)
        self.n = self.p * self.q
        self.n_square = self.n ** 2
        self.lambda_ = (self.p - 1) * (self.q - 1) // math.gcd(self.p - 1, self.q - 1)
        self.g = self.n + 1
        self.mu = pow(self._l(pow(self.g, self.lambda_, self.n_square), self.n), -1, self.n)

    def generate_prime(self, bits):
        while True:
            n = random.getrandbits(bits) | 1
            if self.is_prime(n):
                return n

    def is_prime(self, n, k=10):
        if n < 2:
            return False
        for _ in range(k):
            a = random.randrange(2, n)
            if pow(a, n-1, n) != 1:
                return False
        return True

    def _l(self, x, n):
        return (x - 1) // n

    def encrypt(self, m):
        if m >= self.n:
            raise ValueError("Message too large")
        while True:
            r = random.randrange(1, self.n)
            if math.gcd(r, self.n) == 1:
                break
        return (pow(self.g, m, self.n_square) * pow(r, self.n, self.n_square)) % self.n_square

    def decrypt(self, c):
        return (self._l(pow(c, self.lambda_, self.n_square), self.n) * self.mu) % self.n

    def add(self, c1, c2):
        return (c1 * c2) % self.n_square

# ElGamal Implementation
class ElGamal:
    def __init__(self, bit_length=256):
        self.p = self.generate_prime(bit_length)
        self.g = random.randrange(3, self.p)
        while pow(self.g, (self.p-1)//2, self.p) == 1:  # Simple generator check
            self.g = random.randrange(3, self.p)
        self.x = random.randrange(3, self.p-1)
        self.y = pow(self.g, self.x, self.p)

    def generate_prime(self, bits):
        while True:
            n = random.getrandbits(bits) | 1
            if self.is_prime(n):
                return n

    def is_prime(self, n, k=10):
        if n < 2:
            return False
        for _ in range(k):
            a = random.randrange(2, n)
            if pow(a, n-1, n) != 1:
                return False
        return True

    def encrypt(self, m):
        if m >= self.p:
            raise ValueError("Message too large")
        r = random.randrange(1, self.p-1)
        c1 = pow(self.g, r, self.p)
        c2 = (m * pow(self.y, r, self.p)) % self.p
        return c1, c2

    def decrypt(self, c1, c2):
        return (c2 * pow(c1, self.p - 1 - self.x, self.p)) % self.p

    def multiply(self, ct1, ct2):
        c1_1, c2_1 = ct1
        c1_2, c2_2 = ct2
        return (c1_1 * c1_2 % self.p, c2_1 * c2_2 % self.p)

def shamir_share(secret, n, t, prime):
    coeffs = [secret] + [random.randrange(1, prime) for _ in range(t-1)]
    shares = []
    for i in range(1, n+1):
        share = sum(coeff * (i ** exp) for exp, coeff in enumerate(coeffs)) % prime
        shares.append((i, share))
    return shares

def shamir_reconstruct(shares, prime):
    t = len(shares)
    secret = 0
    for j, (_, yj) in enumerate(shares):
        lj = 1
        for k, (xk, _) in enumerate(shares):
            if k != j:
                lj = (lj * (xk * pow(xk - shares[j][0], -1, prime) % prime)) % prime
                lj = (lj * pow(xk - shares[j][0], -1, prime)) % prime
        secret = (secret + yj * lj) % prime
    return secret

class ThresholdPaillier(Paillier):
    def __init__(self, bit_length=256, n_parties=3, threshold=2):
        super().__init__(bit_length)
        self.n_parties = n_parties
        self.threshold = threshold
        self.prime_for_share = self.generate_prime(bit_length + 64)
        self.shares = shamir_share(self.lambda_, n_parties, threshold, self.prime_for_share)

    def partial_decrypt(self, c, party_id):
        i, share = self.shares[party_id - 1]
        partial = pow(c, share, self.n_square)
        return partial

    def combine_partials(self, partials, party_ids):
        delta = math.factorial(self.n_parties)
        combined = 1
        for j in range(len(partials)):
            l_j = delta
            for k in range(len(partials)):
                if k != j:
                    l_j //= (party_ids[j] - party_ids[k])
            combined = (combined * pow(partials[j], 2 * l_j, self.n_square)) % self.n_square
        m = (self._l(combined, self.n) * self.mu) % self.n
        return m

def exercise_1a():
    print("\n1a: Homomorphic Multiplication with ElGamal")
    elgamal = ElGamal()
    m1, m2 = 7, 3
    ct1 = elgamal.encrypt(m1)
    ct2 = elgamal.encrypt(m2)
    print(f"Ciphertext1: {ct1}")
    print(f"Ciphertext2: {ct2}")
    ct_prod = elgamal.multiply(ct1, ct2)
    print(f"Encrypted Product: {ct_prod}")
    dec_prod = elgamal.decrypt(*ct_prod)
    expected = (m1 * m2) % elgamal.p
    print(f"Decrypted: {dec_prod}, Expected: {expected}")
    print(f"Verification: {'Correct' if dec_prod == expected else 'Incorrect'}")

def exercise_1b():
    print("\n1b: Secure Data Sharing with Paillier")
    paillier = Paillier()
    alice_data = 15000
    bob_data = 25000
    c_bob = paillier.encrypt(bob_data)
    c_alice = paillier.encrypt(alice_data)
    c_sum = paillier.add(c_alice, c_bob)
    total = paillier.decrypt(c_sum)
    print(f"Encrypted Sum: {c_sum}")
    print(f"Decrypted Total: {total}, Expected: {alice_data + bob_data}")
    print("Alice learns total without knowing Bob's individual data.")

def exercise_1c():
    print("\n1c: Secure Thresholding with Paillier")
    t_paillier = ThresholdPaillier(n_parties=3, threshold=2)
    values = [10, 20, 30]
    c_sum = 1
    for v in values:
        c_v = t_paillier.encrypt(v)
        c_sum = t_paillier.add(c_sum, c_v)
    print(f"Encrypted Combined: {c_sum}")
    partial1 = t_paillier.partial_decrypt(c_sum, 1)
    partial2 = t_paillier.partial_decrypt(c_sum, 2)
    partials = [partial1, partial2]
    party_ids = [1, 2]
    dec_sum = t_paillier.combine_partials(partials, party_ids)
    expected = sum(values)
    print(f"Threshold Decrypted: {dec_sum}, Expected: {expected}")
    print(f"Verification: {'Correct' if dec_sum == expected else 'Incorrect'}")

def exercise_1d():
    print("\n1d: Performance Benchmarking")
    def bench_paillier():
        p = Paillier(bit_length=128)
        m = 15
        c = p.encrypt(m)
        p.decrypt(c)
        p.add(c, c)

    def bench_elgamal():
        e = ElGamal(bit_length=128)
        m = 7
        ct = e.encrypt(m)
        e.decrypt(*ct)
        e.multiply(ct, ct)

    t_paillier = timeit.timeit(bench_paillier, number=10)
    t_elgamal = timeit.timeit(bench_elgamal, number=10)
    print(f"Paillier average time (10 runs): {t_paillier / 10:.6f}s")
    print(f"ElGamal average time (10 runs): {t_elgamal / 10:.6f}s")
    print("Note: Paillier typically slower in encryption due to larger ops.")

if __name__ == "__main__":
    exercise_1a()
    exercise_1b()
    exercise_1c()
    exercise_1d()