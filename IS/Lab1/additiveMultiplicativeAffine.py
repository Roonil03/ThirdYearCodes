import string

plain = "I am learning information security".replace(" ", "").lower()
alpha = string.ascii_lowercase
m = 26

def add_enc(t, k):
    return "".join(alpha[(alpha.index(c) + k) % m] if c in alpha else c for c in t)

def add_dec(c, k):
    return "".join(alpha[(alpha.index(ch) - k) % m] if ch in alpha else ch for ch in c)

def mul_inv(a, mod):
    for x in range(1, mod):
        if (a * x) % mod == 1:
            return x
    raise ValueError

def mul_enc(t, k):
    return "".join(alpha[(alpha.index(c) * k) % m] if c in alpha else c for c in t)

def mul_dec(c, k):
    inv = mul_inv(k, m)
    return "".join(alpha[(alpha.index(ch) * inv) % m] if ch in alpha else ch for ch in c)

def aff_enc(t, a, b):
    return "".join(alpha[(a * alpha.index(c) + b) % m] if c in alpha else c for c in t)

def aff_dec(c, a, b):
    inv = mul_inv(a, m)
    return "".join(alpha[(inv * (alpha.index(ch) - b)) % m] if ch in alpha else ch for ch in c)

add_key = 20
mul_key = 15
aff_a, aff_b = 15, 20

c_add = add_enc(plain, add_key)
d_add = add_dec(c_add, add_key)

c_mul = mul_enc(plain, mul_key)
d_mul = mul_dec(c_mul, mul_key)

c_aff = aff_enc(plain, aff_a, aff_b)
d_aff = aff_dec(c_aff, aff_a, aff_b)

print("Additive cipher:", c_add)
print("Decrypted:", d_add)
print("Multiplicative cipher:", c_mul)
print("Decrypted:", d_mul)
print("Affine cipher:", c_aff)
print("Decrypted:", d_aff)
