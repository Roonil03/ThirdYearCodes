import socket

def djb2_hash(input_bytes: bytes) -> int:
    hash_value = 5381
    mask_32bit = 0xFFFFFFFF
    for b in input_bytes:
        hash_value = ((hash_value << 5) + hash_value + b) & mask_32bit
    return hash_value

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
BUFFER_SIZE = 4  # Expecting 4 bytes for 32-bit hash

def send_and_verify(message: str) -> None:
    data = message.encode('utf-8')
    local_hash = djb2_hash(data)
    print(f"[<] Sending message: {message!r}")
    print(f"[<] Local hash: {local_hash:#010x}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.sendall(data)

        # Receive 4-byte hash from server
        resp = sock.recv(BUFFER_SIZE)
        if len(resp) < 4:
            print("[-] Incomplete hash received.")
            return
        server_hash = int.from_bytes(resp, byteorder='big')
        print(f"[>] Server hash: {server_hash:#010x}")

    if local_hash == server_hash:
        print("[✓] Integrity verified: hashes match.")
    else:
        print("[✗] Integrity check failed: hashes do not match!")

if __name__ == "__main__":
    # Example: correct transmission
    send_and_verify("Hello, secure world!")

    # Example: simulate tampering (client intentionally modifies data after computing hash)
    print("\n--- Simulating tampering ---")
    original = "Message to tamper"
    data = original.encode('utf-8')
    local_hash = djb2_hash(data)
    tampered_data = b"Tampered message"
    print(f"[<] Pretending to send original message {original!r} but actually sending tampered data.")
    print(f"[<] Local hash computed on original: {local_hash:#010x}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.sendall(tampered_data)
        resp = sock.recv(BUFFER_SIZE)
        server_hash = int.from_bytes(resp, byteorder='big')
        print(f"[>] Server hash (on tampered data): {server_hash:#010x}")

    if local_hash == server_hash:
        print("[✗] Integrity erroneously passed.")
    else:
        print("[✓] Integrity check correctly detected tampering.")
