import socket
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random.random import randint
from Crypto.Hash import SHA256

P = 23
G = 5

def dh_generate_private():
    return randint(1, P - 1)

def dh_generate_public(private):
    return pow(G, private, P)

def dh_generate_shared(public, private):
    return pow(public, private, P)

def get_aes_key(shared_secret):
    sha = SHA256.new()
    sha.update(str(shared_secret).encode())
    return sha.digest()[:16]

s = socket.socket()
s.bind(('localhost', 12345))
s.listen(1)
print("Server listening...")

conn, addr = s.accept()
print("Connected by", addr)

server_private = dh_generate_private()
server_public = dh_generate_public(server_private)

client_public = int(conn.recv(1024).decode())
conn.send(str(server_public).encode())

shared = dh_generate_shared(client_public, server_private)
aes_key = get_aes_key(shared)

# Receive encrypted message
data = json.loads(conn.recv(1024).decode())
ciphertext = bytes.fromhex(data['ciphertext'])
iv = bytes.fromhex(data['iv'])

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
message = unpad(cipher.decrypt(ciphertext), AES.block_size)
print("Decrypted message:", message.decode())

conn.close()
