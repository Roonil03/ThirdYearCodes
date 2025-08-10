from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

pt = "Encryption Strength"
k = "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF"
key = bytes.fromhex(k)

print(f"Plaintext: {pt}")
print(f"Key (hex): {k}")

cipher = AES.new(key, AES.MODE_ECB)

padded_message = pad(pt.encode(), AES.block_size)
print(f"Padded message length: {len(padded_message)} bytes")

ct = cipher.encrypt(padded_message)
print(f"Ciphertext (hex): {ct.hex()}")

mes = unpad(cipher.decrypt(ct), AES.block_size).decode()
print(f"Decrypted message: {mes}")

print(f"Original == Decrypted: {pt == mes}")
