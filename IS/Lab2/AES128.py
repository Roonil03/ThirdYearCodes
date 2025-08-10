from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key_hex = "0123456789ABCDEF0123456789ABCDEF"
key = bytes.fromhex(key_hex)

pt = "Sensitive Information"
print(f"Plaintext: {pt}")

cipher = AES.new(key, AES.MODE_ECB)

p = pad(pt.encode(), AES.block_size)
print(f"Padded Message (bytes): {p}")

ct = cipher.encrypt(p)
print(f"Ciphertext (hex): {ct.hex()}")

mes = unpad(cipher.decrypt(ct), AES.block_size).decode()
print(f"Decrypted Message: {mes}")

print(f"\nVerification: {pt == mes}")
