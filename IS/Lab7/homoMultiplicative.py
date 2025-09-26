import math


class RSA:
    def __init__(self):
        self.p = 61
        self.q = 53
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 17  # gcd(17, 3120) = 1
        self.d = pow(self.e, -1, self.phi)

    def encrypt(self, m):
        if m >= self.n:
            raise ValueError("Message must be less than n")
        return pow(m, self.e, self.n)

    def decrypt(self, c):
        return pow(c, self.d, self.n)

    def multiply(self, c1, c2):
        return (c1 * c2) % self.n

rsa = RSA()
m1 = 7
m2 = 3
c1 = rsa.encrypt(m1)
c2 = rsa.encrypt(m2)
print(f"Original integers: {m1}, {m2}")
print(f"Ciphertext of {m1}: {c1}")
print(f"Ciphertext of {m2}: {c2}")
c_prod = rsa.multiply(c1, c2)
print(f"Encrypted product: {c_prod}")
decrypted_prod = rsa.decrypt(c_prod)
print(f"Decrypted product: {decrypted_prod}")
expected_prod = (m1 * m2) % rsa.n
print(f"Expected product: {expected_prod}")
print(f"Verification: {'Correct' if decrypted_prod == expected_prod else 'Incorrect'}")