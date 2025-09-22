from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import json

def generate_elgamal_keys():
    key = ElGamal.generate(2048, get_random_bytes)
    return key

def encrypt_elgamal(public_key, message):
    session_key = get_random_bytes(16)
    cipher = AES.new(session_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = cipher.iv

    # Encrypt session key using ElGamal
    k = randint(1, public_key.p - 2)
    a = pow(public_key.g, k, public_key.p)
    b = (public_key.y ** k * int.from_bytes(session_key, byteorder='big')) % public_key.p
    return {
        'a': a,
        'b': b,
        'iv': iv.hex(),
        'ciphertext': ct_bytes.hex()
    }

def decrypt_elgamal(private_key, encrypted_data):
    a = encrypted_data['a']
    b = encrypted_data['b']
    iv = bytes.fromhex(encrypted_data['iv'])
    ct = bytes.fromhex(encrypted_data['ciphertext'])

    s = pow(a, private_key.x, private_key.p)
    s_inv = pow(s, -1, private_key.p)
    session_key = (b * s_inv) % private_key.p
    session_key_bytes = session_key.to_bytes(16, byteorder='big')

    cipher = AES.new(session_key_bytes, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

# Usage
key = generate_elgamal_keys()
public_key = key.publickey()
msg = "Hello from ElGamal"
encrypted = encrypt_elgamal(public_key, msg)
decrypted = decrypt_elgamal(key, encrypted)

print("Original:", msg)
print("Decrypted:", decrypted)
