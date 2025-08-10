pt = "Cryptographic Protocols"
n = 323
e = 5
d = 173


def string_to_int(text):
    return int.from_bytes(text.encode(), 'big')

def int_to_string(num):
    byte_length = (num.bit_length() + 7) // 8
    if byte_length == 0:
        byte_length = 1
    return num.to_bytes(byte_length, 'big').decode()

def string_to_chunks(text, max_value):
    chunks = []
    text_bytes = text.encode()
    chunk_size = 1
    for i in range(0, len(text_bytes), chunk_size):
        chunk_bytes = text_bytes[i:i + chunk_size]
        chunk_int = int.from_bytes(chunk_bytes, 'big')
        while chunk_int >= max_value and len(chunk_bytes) > 1:
            chunk_size = len(chunk_bytes) - 1
            chunk_bytes = chunk_bytes[:chunk_size]
            chunk_int = int.from_bytes(chunk_bytes, 'big')
        if chunk_int < max_value:
            chunks.append(chunk_int)
        else:
            chunks.append(chunk_int % max_value)
    return chunks

def chunks_to_string(chunks):
    text_bytes = b''
    for chunk_int in chunks:
        if chunk_int == 0:
            text_bytes += b'\x00'
        else:
            byte_length = (chunk_int.bit_length() + 7) // 8
            chunk_bytes = chunk_int.to_bytes(byte_length, 'big')
            text_bytes += chunk_bytes
    return text_bytes.decode(errors='ignore')


print(f"Plaintext: {pt}")
print(f"RSA parameters: n={n}, e={e}, d={d}")

msg_int = string_to_int(pt)
print(f"Message as integer: {msg_int}")
print(f"Message > n: {msg_int > n}")

msg_chunks = string_to_chunks(pt, n)
print(f"Message chunks: {msg_chunks}")
print(f"Number of chunks: {len(msg_chunks)}")

encrypted_chunks = []

for i, chunk in enumerate(msg_chunks):
    if chunk >= n:
        print(f"Error: Chunk {i} ({chunk}) >= n ({n})")
        continue
    ct_chunk = pow(chunk, e, n)
    encrypted_chunks.append(ct_chunk)
    print(f"Chunk {i}: {chunk} -> {ct_chunk}")

print(f"Encrypted chunks: {encrypted_chunks}")

decrypted_chunks = []
for i, ct_chunk in enumerate(encrypted_chunks):
    decrypted_chunk = pow(ct_chunk, d, n)
    decrypted_chunks.append(decrypted_chunk)
    print(f"Chunk {i}: {ct_chunk} -> {decrypted_chunk}")

print(f"Decrypted chunks: {decrypted_chunks}")

mes = chunks_to_string(decrypted_chunks)
print(f"Decrypted message: {mes}")

print(f"Original == Decrypted: {pt == mes}")
print(f"Original chunks: {msg_chunks}")
print(f"Decrypted chunks: {decrypted_chunks}")

print(f"n = {n}")
print(f"e = {e}")
print(f"d = {d}")
print(f"e * d mod φ(n): {(e * d) % ((323 // 17) - 1) * (17 - 1)}")
