from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

k = "A1B2C3D4E5F60708"
key = bytes.fromhex(k)

block1_hex = "54686973206973206120636f6e666964656e7469616c206d657373616765"
block2_hex = "416e64207468697320697320746865207365636f6e6420626c6f636b"

block1 = bytes.fromhex(block1_hex)
block2 = bytes.fromhex(block2_hex)

print(f"Key (hex): {k}")
print(f"Key length: {len(key)} bytes")
print(f"Block1 (hex): {block1_hex}")
print(f"Block2 (hex): {block2_hex}")
print(f"Block1 (text): {block1.decode()}")
print(f"Block2 (text): {block2.decode()}")

cipher = DES.new(key, DES.MODE_ECB)
p1 = pad(block1, DES.block_size)
p2 = pad(block2, DES.block_size)

print(f"\nENCRYPTION")
ct1 = cipher.encrypt(p1)
ct2 = cipher.encrypt(p2)
print(f"Block1(hex): {ct1.hex()}")
print(f"Block2(hex): {ct2.hex()}")

print(f"\nDECRYPTION")
dt1 = unpad(cipher.decrypt(ct1), DES.block_size)
dt2 = unpad(cipher.decrypt(ct2), DES.block_size)
print(f"Block1(hex): {dt1.hex()}")
print(f"Block2(hex): {dt2.hex()}")
print(f"Block1(text): {dt1.decode()}")
print(f"Block2(text): {dt2.decode()}")

print(f"\nVERIFICATION")
print(f"Block1: {block1 == dt1}")
print(f"Block2: {block2 == dt2}")
