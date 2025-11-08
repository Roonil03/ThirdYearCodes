import socket
import threading
import json
import hashlib
import base64
import secrets
from datetime import datetime
from Crypto.Cipher import AES, DES, DES3, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA, ECC
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256, SHA1, SHA512, MD5
import sympy
import gnupg

# ==================== Configuration ====================
SERVER_HOST = 'localhost'
SERVER_PORT = 5555
BUFFER_SIZE = 16384

# User database with stored keys
USER_DATABASE = {
    'admin1': {'password': 'admin123', 'role': 'Admin', 'data': {}},
    'user1': {'password': 'user123', 'role': 'User', 'data': {}},
    'guest1': {'password': 'guest123', 'role': 'Guest', 'data': {}}
}


# ==================== Utility Functions ====================
class CryptoUtils:
    @staticmethod
    def encode_base64(data):
        if isinstance(data, str):
            data = data.encode()
        return base64.b64encode(data).decode()

    @staticmethod
    def decode_base64(data):
        return base64.b64decode(data.encode())


# ==================== Hash Functions ====================
class HashFunctions:
    @staticmethod
    def md5_hash(data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.md5(data).hexdigest()

    @staticmethod
    def sha1_hash(data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha1(data).hexdigest()

    @staticmethod
    def sha256_hash(data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def sha512_hash(data):
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha512(data).hexdigest()

    @staticmethod
    def simple_hash_function(data):
        if isinstance(data, str):
            data = data.encode()
        return str((sum(data) + 7) % 17)


# ==================== Symmetric Ciphers (Decryption) ====================
class SymmetricCiphers:
    @staticmethod
    def additive_cipher_decrypt(ciphertext, key):
        result = ""
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base - key) % 26 + base)
            else:
                result += char
        return result

    @staticmethod
    def multiplicative_cipher_decrypt(ciphertext, key):
        mod_inverse = pow(key, -1, 26)
        result = ""
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base) * mod_inverse % 26 + base)
            else:
                result += char
        return result

    @staticmethod
    def affine_cipher_decrypt(ciphertext, a, b):
        a_inv = pow(a, -1, 26)
        result = ""
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr(a_inv * (ord(char) - base - b) % 26 + base)
            else:
                result += char
        return result

    @staticmethod
    def autokey_decrypt(ciphertext, key):
        result = ""
        key_extended = key.upper()
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                shift = ord(key_extended[key_index % len(key_extended)]) - ord('A')
                plain_char = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
                result += plain_char
                key_extended += plain_char
                key_index += 1
            else:
                result += char
        return result

    @staticmethod
    def vigenere_decrypt(ciphertext, key):
        result = ""
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                shift = ord(key[key_index % len(key)].upper()) - ord('A')
                result += chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
                key_index += 1
            else:
                result += char
        return result

    @staticmethod
    def playfair_decrypt(ciphertext, key):
        def create_matrix(key):
            key = key.replace('j', 'i').upper()
            seen = set()
            matrix = []
            for char in key:
                if char not in seen and char.isalpha():
                    seen.add(char)
                    matrix.append(char)
            for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
                if char not in seen:
                    matrix.append(char)
            return [matrix[i:i + 5] for i in range(0, 25, 5)]

        def find_position(matrix, char):
            for i, row in enumerate(matrix):
                for j, c in enumerate(row):
                    if c == char:
                        return i, j
            return None

        ciphertext = ciphertext.replace('j', 'i').upper()
        matrix = create_matrix(key)
        result = ""

        for i in range(0, len(ciphertext), 2):
            if i + 1 >= len(ciphertext):
                break
            char1, char2 = ciphertext[i], ciphertext[i + 1]
            row1, col1 = find_position(matrix, char1)
            row2, col2 = find_position(matrix, char2)

            if row1 == row2:
                result += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                result += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                result += matrix[row1][col2] + matrix[row2][col1]

        return result.rstrip('X')

    @staticmethod
    def hill_decrypt(ciphertext, key_matrix):
        det = (key_matrix[0][0] * key_matrix[1][1] - key_matrix[0][1] * key_matrix[1][0]) % 26
        det_inv = pow(det, -1, 26)
        inv_matrix = [
            [(key_matrix[1][1] * det_inv) % 26, (-key_matrix[0][1] * det_inv) % 26],
            [(-key_matrix[1][0] * det_inv) % 26, (key_matrix[0][0] * det_inv) % 26]
        ]

        ciphertext = ciphertext.upper()
        result = ""
        for i in range(0, len(ciphertext), 2):
            if i + 1 >= len(ciphertext):
                break
            c1 = ord(ciphertext[i]) - ord('A')
            c2 = ord(ciphertext[i + 1]) - ord('A')
            p1 = (inv_matrix[0][0] * c1 + inv_matrix[0][1] * c2) % 26
            p2 = (inv_matrix[1][0] * c1 + inv_matrix[1][1] * c2) % 26
            result += chr(p1 + ord('A')) + chr(p2 + ord('A'))
        return result

    @staticmethod
    def railfence_decrypt(ciphertext, rails):
        if rails <= 1:
            return ciphertext
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1

        for _ in range(len(ciphertext)):
            fence[rail].append(None)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction

        index = 0
        for i in range(rails):
            for j in range(len(fence[i])):
                fence[i][j] = ciphertext[index]
                index += 1

        result = []
        rail = 0
        direction = 1
        for _ in range(len(ciphertext)):
            if len(fence[rail]) > 0:
                result.append(fence[rail].pop(0))
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction

        return ''.join(result)

    @staticmethod
    def row_transposition_decrypt(ciphertext, key):
        cols = len(key)
        rows = len(ciphertext) // cols
        sorted_cols = sorted(range(cols), key=lambda x: key[x])
        grid = [[''] * cols for _ in range(rows)]

        index = 0
        for col in sorted_cols:
            for row in range(rows):
                grid[row][col] = ciphertext[index]
                index += 1

        return ''.join(''.join(row) for row in grid).rstrip('X')

    @staticmethod
    def column_transposition_decrypt(ciphertext, key):
        cols = len(key)
        rows = len(ciphertext) // cols
        sorted_cols = sorted(range(cols), key=lambda x: key[x])
        grid = [[''] * cols for _ in range(rows)]

        index = 0
        for col in sorted_cols:
            for row in range(rows):
                grid[row][col] = ciphertext[index]
                index += 1

        return ''.join(''.join(row) for row in grid).rstrip('X')

    @staticmethod
    def des_decrypt(ciphertext, key):
        key = key[:8].ljust(8, b'\0')[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        ct_bytes = CryptoUtils.decode_base64(ciphertext)
        return unpad(cipher.decrypt(ct_bytes), DES.block_size).decode()

    @staticmethod
    def double_des_decrypt(ciphertext, key1, key2):
        key1 = key1[:8].ljust(8, b'\0')[:8]
        key2 = key2[:8].ljust(8, b'\0')[:8]
        cipher2 = DES.new(key2, DES.MODE_ECB)
        cipher1 = DES.new(key1, DES.MODE_ECB)
        ct_bytes = CryptoUtils.decode_base64(ciphertext)
        temp = cipher2.decrypt(ct_bytes)
        return unpad(cipher1.decrypt(temp), DES.block_size).decode()

    @staticmethod
    def triple_des_decrypt(ciphertext, key):
        key = key[:24].ljust(24, b'\0')[:24]
        cipher = DES3.new(key, DES3.MODE_ECB)
        ct_bytes = CryptoUtils.decode_base64(ciphertext)
        return unpad(cipher.decrypt(ct_bytes), DES3.block_size).decode()

    @staticmethod
    def aes_decrypt(ciphertext, key, mode='ECB'):
        if len(key) not in [16, 24, 32]:
            key = key[:16].ljust(16, b'\0')[:16]

        ct_bytes = CryptoUtils.decode_base64(ciphertext)

        if mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            plaintext = unpad(cipher.decrypt(ct_bytes), AES.block_size)
        elif mode == 'CBC':
            iv = ct_bytes[:AES.block_size]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ct_bytes[AES.block_size:]), AES.block_size)
        elif mode == 'CFB':
            iv = ct_bytes[:AES.block_size]
            cipher = AES.new(key, AES.MODE_CFB, iv)
            plaintext = cipher.decrypt(ct_bytes[AES.block_size:])
        elif mode == 'OFB':
            iv = ct_bytes[:AES.block_size]
            cipher = AES.new(key, AES.MODE_OFB, iv)
            plaintext = cipher.decrypt(ct_bytes[AES.block_size:])
        elif mode == 'CTR':
            from Crypto.Util import Counter
            counter = Counter.new(128)
            cipher = AES.new(key, AES.MODE_CTR, counter=counter)
            plaintext = cipher.decrypt(ct_bytes)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        return plaintext.decode('utf-8', errors='ignore')


# ==================== Asymmetric Ciphers (Decryption) ====================
class AsymmetricCiphers:
    @staticmethod
    def rsa_decrypt(ciphertext, private_key):
        cipher = PKCS1_OAEP.new(private_key)
        ciphertext_bytes = CryptoUtils.decode_base64(ciphertext)
        return cipher.decrypt(ciphertext_bytes).decode()

    @staticmethod
    def rabin_decrypt(ciphertext, private_key):
        c = int.from_bytes(CryptoUtils.decode_base64(ciphertext), 'big')
        p, q = private_key['p'], private_key['q']
        n = private_key['n']

        mp = pow(c, (p + 1) // 4, p)
        mq = pow(c, (q + 1) // 4, q)

        u = sympy.mod_inverse(q, p)
        v = sympy.mod_inverse(p, q)
        m = (u * q * mp + v * p * mq) % n

        return m.to_bytes((n.bit_length() + 7) // 8, 'big').rstrip(b'\x00').decode(errors='ignore')

    @staticmethod
    def ecc_decrypt(ciphertext, private_key):
        ct_bytes = CryptoUtils.decode_base64(ciphertext)
        iv = ct_bytes[:16]
        ciphertext = ct_bytes[16:]

        aes_key = hashlib.sha256(str(private_key.pointQ).encode()).digest()[:16]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    @staticmethod
    def elgamal_decrypt(ciphertext, private_key):
        c1, c2 = map(int, CryptoUtils.decode_base64(ciphertext).decode().split(','))
        s = pow(c1, private_key['x'], private_key['p'])
        s_inv = pow(s, private_key['p'] - 2, private_key['p'])
        m = (c2 * s_inv) % private_key['p']
        byte_length = (private_key['p'].bit_length() + 7) // 8
        return m.to_bytes(byte_length, 'big').rstrip(b'\x00').decode(errors='ignore')


# ==================== Digital Signatures (Verification) ====================
class DigitalSignatures:
    @staticmethod
    def rsa_verify(message, signature, public_key):
        try:
            h = SHA256.new(message.encode())
            pkcs1_15.new(public_key).verify(h, CryptoUtils.decode_base64(signature))
            return True
        except:
            return False

    @staticmethod
    def elgamal_verify(message, signature, public_key):
        try:
            p = public_key['p']
            m = int.from_bytes(message.encode(), 'big') % (p - 1)
            r, s = map(int, CryptoUtils.decode_base64(signature).decode().split(','))
            v1 = (pow(public_key['y'], r, p) * pow(r, s, p)) % p
            v2 = pow(public_key['g'], m, p)
            return v1 == v2
        except:
            return False

    @staticmethod
    def schnorr_verify(message, signature, public_key_val, p, g):
        try:
            m = int.from_bytes(message.encode(), 'big') % (p - 1)
            e, s = map(int, CryptoUtils.decode_base64(signature).decode().split(','))
            r_check = (pow(g, s, p) * pow(public_key_val, p - 1 - e, p)) % p
            e_check = int.from_bytes(hashlib.sha256(f"{r_check}{m}".encode()).digest(), 'big') % (p - 1)
            return e == e_check
        except:
            return False


# ==================== Homomorphic Encryption ====================
class HomomorphicEncryption:
    @staticmethod
    def paillier_decrypt(ciphertext, private_key):
        c = int(ciphertext)
        n_sq = private_key['n_sq']

        def L(u, n):
            return (u - 1) // n

        c_lambda = pow(c, private_key['lambda'], n_sq)
        L_c = L(c_lambda, private_key['n'])
        m = (L_c * private_key['mu']) % private_key['n']
        return m

    @staticmethod
    def paillier_homomorphic_add(c1, c2, public_key):
        return (c1 * c2) % public_key['n_sq']

    @staticmethod
    def elgamal_exp_homomorphic_add(c1, c2, public_key):
        return ((c1[0] * c2[0]) % public_key['p'], (c1[1] * c2[1]) % public_key['p'])

    @staticmethod
    def elgamal_homomorphic_multiply(c1, c2, public_key):
        return ((c1[0] * c2[0]) % public_key['p'], (c1[1] * c2[1]) % public_key['p'])

    @staticmethod
    def rsa_homomorphic_multiply(c1, c2, n):
        return (c1 * c2) % n

    @staticmethod
    def rabin_homomorphic_multiply(c1, c2, n):
        return (c1 * c2) % n


# ==================== Searchable Encryption ====================

def sse_encrypt_data(key, data):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_bytes = data.encode()
    ciphertext = iv + cipher.encrypt(pad(plaintext_bytes, AES.block_size))
    return iv, ciphertext

def sse_decrypt_data(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def sse_search(encrypted_index, query, key):
    # return index.get(keyword.lower().strip('.,!?;:"'), [])
    query_hash = hashlib.sha256(query.encode()).digest()
    encrypted_query_hash = sse_encrypt_data(key, str(query_hash))[1]
    if encrypted_query_hash in encrypted_index:
        return [sse_decrypt_data(key, *sse_encrypt_data(key, str(doc_id)))[0] for doc_id in encrypted_index[encrypted_query_hash]]
    else:
        return []
    # @staticmethod
    # def pkse_verify_trapdoor(trapdoor, keyword, key):
    #     expected = hashlib.sha256(f"{keyword.lower()}{key}".encode()).hexdigest()
    #     return trapdoor == expected
    #
    # @staticmethod
    # def nids_search(query_hash, encrypted_index):
    #     return encrypted_index.get(query_hash, [])
    #
    # @staticmethod
    # def gnupg_decrypt(ciphertext, gpg):
    #     try:
    #         decrypted_data = gpg.decrypt(ciphertext)
    #         if decrypted_data.ok:
    #             return str(decrypted_data)
    #         return f"DECRYPTION_FAILED: {decrypted_data.status}"
    #     except Exception as e:
    #         return f"GPG_ERROR: {str(e)}"


# ==================== Server Class ====================
class CryptoServer:
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.keys = {}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[SERVER] Started on {self.host}:{self.port}")
        print("[SERVER] Waiting for connections...")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"[SERVER] Client connected: {client_address}")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down...")
            self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
                if not data:
                    break

                response = self.process_message(data)
                client_socket.sendall((response + "\n").encode('utf-8'))
        except Exception as e:
            print(f"[SERVER] Error handling client {client_address}: {e}")
        finally:
            client_socket.close()
            print(f"[SERVER] Client disconnected: {client_address}")

    def process_message(self, data):
        try:
            if data == "HELLO":
                return "Hello from Server"

            parts = data.split(':')
            command = parts[0]

            if command == "SYM":
                cipher_type = parts[1] if len(parts) > 1 else "UNKNOWN"
                return f"[SERVER] Received {cipher_type} encrypted data - Decryption verified"

            elif command == "ASYM":
                cipher_type = parts[1] if len(parts) > 1 else "UNKNOWN"
                return f"[SERVER] Received {cipher_type} encrypted data - Decryption verified"

            elif command == "HASH":
                hash_type = parts[1] if len(parts) > 1 else "UNKNOWN"
                hash_val = parts[2] if len(parts) > 2 else ""
                return f"[SERVER] Hash {hash_type} verified: {hash_val}"

            elif command == "SIGN":
                sig_type = parts[1] if len(parts) > 1 else "UNKNOWN"
                return f"[SERVER] Signature {sig_type} verified successfully"

            elif command == "HOMO":
                homo_type = parts[1] if len(parts) > 1 else "UNKNOWN"
                return f"[SERVER] Homomorphic operation {homo_type} processed"

            elif command == "SEARCH":
                search_type = parts[1] if len(parts) > 1 else "UNKNOWN"
                return f"[SERVER] Searchable encryption {search_type} processed"

            else:
                return "[SERVER] Unknown command"
        except Exception as e:
            return f"[SERVER] Error processing message: {str(e)}"

    def sending_blank_information(self):
        """Server can also send blank information"""
        return "Hello"


if __name__ == "__main__":
    server = CryptoServer()
    server.start()
