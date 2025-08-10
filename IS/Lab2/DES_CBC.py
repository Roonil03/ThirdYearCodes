from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

pt = "Secure Communication"
k = "A1B2C3D4"
iv = "12345678"

key = k.encode()
i = iv.encode()

print(f"Plaintext: {pt}")
print(f"Key: {k}")
print(f"IV: {iv}")

cipher = DES.new(key, DES.MODE_CBC, i)
p = pad(pt.encode(), DES.block_size)
ct = cipher.encrypt(p)
print(f"Ciphertext (hex): {ct.hex()}")

cipher_decrypt = DES.new(key, DES.MODE_CBC, i)
mes = unpad(cipher_decrypt.decrypt(ct), DES.block_size).decode()
print(f"Decrypted message: {mes}")

print(f"Original == Decrypted: {pt == mes}")
