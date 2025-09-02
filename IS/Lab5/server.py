import socket
from typing import Tuple

def djb2_hash(input_bytes: bytes) -> int:
    hash_value = 5381
    mask_32bit = 0xFFFFFFFF
    for b in input_bytes:
        hash_value = ((hash_value << 5) + hash_value + b) & mask_32bit
    return hash_value

HOST = '0.0.0.0'
PORT = 5000
BUFFER_SIZE = 4096

def handle_client(conn: socket.socket, addr: Tuple[str, int]) -> None:
    print(f"[+] Connection from {addr}")
    data = conn.recv(BUFFER_SIZE)
    if not data:
        print("[-] No data received.")
        conn.close()
        return
    server_hash = djb2_hash(data)
    print(f"[>] Received {len(data)} bytes. Computed hash: {server_hash:#010x}")

    conn.sendall(server_hash.to_bytes(4, byteorder='big'))
    conn.close()
    print(f"[+] Connection to {addr} closed.")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    run_server()
