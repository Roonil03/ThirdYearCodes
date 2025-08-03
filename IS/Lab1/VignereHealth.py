import string

plain = "Life is full of surprises".replace(" ", "").lower()
alpha = string.ascii_lowercase
m = 26

def vigenere_enc(text, key):
    key_stream = (key * ((len(text) // len(key)) + 1))[:len(text)]
    return "".join(
        alpha[(alpha.index(c) + alpha.index(k)) % m]
        for c, k in zip(text, key_stream)
    )

vig_key = "health".lower()

ciphertext = vigenere_enc(plain, vig_key)
print("Vigenère cipher:", ciphertext)
