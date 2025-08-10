import random

pt = "Asymmetric Algorithms"
p = 7919
g = 2
h = 6465
x = 2999


def string_to_chunks(text, chunk_size):
    chunks = []
    text_bytes = text.encode()
    for i in range(0, len(text_bytes), chunk_size):
        chunk = text_bytes[i:i + chunk_size]
        chunk_int = int.from_bytes(chunk, 'big')
        chunks.append(chunk_int)
    return chunks


def chunks_to_string(chunks, chunk_size):
    text_bytes = b''
    for chunk_int in chunks:
        byte_length = (chunk_int.bit_length() + 7) // 8
        if byte_length == 0:
            byte_length = 1
        chunk_bytes = chunk_int.to_bytes(byte_length, 'big')
        text_bytes += chunk_bytes
    return text_bytes.decode()


print(f"Plaintext: {pt}")
print(f"Prime p: {p}")
print(f"Generator g: {g}")
print(f"Public key h: {h}")
print(f"Private key x: {x}")

max_chunk_value = p - 1
chunk_size = (max_chunk_value.bit_length() - 1) // 8
print(f"Chunk size: {chunk_size} bytes")

msg_chunks = string_to_chunks(pt, chunk_size)
print(f"Message chunks: {msg_chunks}")

encrypted_chunks = []

for i, chunk in enumerate(msg_chunks):
    if chunk >= p:
        print(f"Error: Chunk {i} ({chunk}) is larger than p ({p})")
        continue

    k = random.randint(2, p - 2)
    c1 = pow(g, k, p)
    c2 = (chunk * pow(h, k, p)) % p
    encrypted_chunks.append((c1, c2))
    print(f"Chunk {i}: k={k}, c1={c1}, c2={c2}")

decrypted_chunks = []
for i, (c1, c2) in enumerate(encrypted_chunks):
    s = pow(c1, x, p)
    s_inv = pow(s, p - 2, p)
    decrypted_chunk = (c2 * s_inv) % p
    decrypted_chunks.append(decrypted_chunk)
    print(f"Chunk {i}: s={s}, s_inv={s_inv}, decrypted={decrypted_chunk}")

mes = chunks_to_string(decrypted_chunks, chunk_size)
print(f"Decrypted message: {mes}")

print(f"Original == Decrypted: {pt == mes}")
print(f"Original chunks: {msg_chunks}")
print(f"Decrypted chunks: {decrypted_chunks}")
