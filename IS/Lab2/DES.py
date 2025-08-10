from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = b'A1B2C3D4'

pt = "Confidential Data"
print(f"Plaintext: {pt}")
cipher = DES.new(key, DES.MODE_ECB)

p = pad(pt.encode(), DES.block_size)
print(f"Padded Message (bytes): {p}")
ct = cipher.encrypt(p)
print(f"Ciphertext (bytes): {ct}")

mes = unpad(cipher.decrypt(ct), DES.block_size).decode()
print(f"Decrypted Message: {mes}")

print(f"\nVerification: {pt == mes}")
