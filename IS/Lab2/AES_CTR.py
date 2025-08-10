from Crypto.Cipher import AES

pt = "Cryptography Lab Exercise"
k = "0123456789ABCDEF0123456789ABCDEF"
nonce = "0000000000000000"

key = bytes.fromhex(k)
nonce_bytes = bytes.fromhex(nonce)

print(f"Plaintext: {pt}")
print(f"Key (hex): {k}")
print(f"Nonce (hex): {nonce}")

cipher = AES.new(key, AES.MODE_CTR, nonce=nonce_bytes)

ct = cipher.encrypt(pt.encode())
print(f"Ciphertext (hex): {ct.hex()}")

cipher_decrypt = AES.new(key, AES.MODE_CTR, nonce=nonce_bytes)
mes = cipher_decrypt.decrypt(ct).decode()
print(f"Decrypted message: {mes}")

print(f"Original == Decrypted: {pt == mes}")
