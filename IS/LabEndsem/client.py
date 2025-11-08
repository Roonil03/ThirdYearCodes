import socket
import json
import hashlib
import base64
import secrets
from datetime import datetime
from Crypto.Cipher import AES, DES, DES3, PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA, ECC
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256, SHA1, SHA512, MD5
import sympy
import gnupg
import random

import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
# ==================== Configuration ====================
SERVER_HOST = 'localhost'
SERVER_PORT = 5555
BUFFER_SIZE = 16384


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


# ==================== Symmetric Ciphers ====================
class SymmetricCiphers:
    # Classical Ciphers
    @staticmethod
    def additive_cipher_encrypt(plaintext, key):
        result = ""
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + key) % 26 + base)
            else:
                result += char
        return result

    @staticmethod
    def multiplicative_cipher_encrypt(plaintext, key):
        result = ""
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base) * key % 26 + base)
            else:
                result += char
        return result

    @staticmethod
    def affine_cipher_encrypt(plaintext, a, b):
        result = ""
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((a * (ord(char) - base) + b) % 26 + base)
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
    def autokey_encrypt(plaintext, key):
        result = ""
        key_extended = key.upper()
        key_index = 0
        for char in plaintext:
            if char.isalpha():
                shift = ord(key_extended[key_index % len(key_extended)]) - ord('A')
                result += chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
                key_extended += char.upper()
                key_index += 1
            else:
                result += char
        return result

    @staticmethod
    def vigenere_encrypt(plaintext, key):
        result = ""
        key_index = 0
        for char in plaintext:
            if char.isalpha():
                shift = ord(key[key_index % len(key)].upper()) - ord('A')
                result += chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
                key_index += 1
            else:
                result += char
        return result

    @staticmethod
    def playfair_encrypt(plaintext, key):
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

        plaintext = plaintext.replace('j', 'i').upper().replace(' ', '')
        if len(plaintext) % 2 != 0:
            plaintext += 'X'

        matrix = create_matrix(key)
        result = ""

        for i in range(0, len(plaintext), 2):
            char1, char2 = plaintext[i], plaintext[i + 1]
            if char1 == char2:
                char2 = 'X'
            row1, col1 = find_position(matrix, char1)
            row2, col2 = find_position(matrix, char2)

            if row1 == row2:
                result += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                result += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                result += matrix[row1][col2] + matrix[row2][col1]
        return result

    @staticmethod
    def hill_encrypt(plaintext, key_matrix):
        plaintext = plaintext.upper().replace(' ', '')
        if len(plaintext) % 2 != 0:
            plaintext += 'X'

        result = ""
        for i in range(0, len(plaintext), 2):
            p1 = ord(plaintext[i]) - ord('A')
            p2 = ord(plaintext[i + 1]) - ord('A')
            c1 = (key_matrix[0][0] * p1 + key_matrix[0][1] * p2) % 26
            c2 = (key_matrix[1][0] * p1 + key_matrix[1][1] * p2) % 26
            result += chr(c1 + ord('A')) + chr(c2 + ord('A'))
        return result

    @staticmethod
    def railfence_encrypt(plaintext, rails):
        if rails <= 1:
            return plaintext
        fence = ['' for _ in range(rails)]
        rail = 0
        direction = 1
        for char in plaintext:
            fence[rail] += char
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        return ''.join(fence)

    @staticmethod
    def row_transposition_encrypt(plaintext, key):
        cols = len(key)
        rows = (len(plaintext) + cols - 1) // cols
        plaintext = plaintext.ljust(rows * cols, 'X')
        grid = [list(plaintext[i * cols:(i + 1) * cols]) for i in range(rows)]
        sorted_cols = sorted(range(cols), key=lambda x: key[x])
        result = ""
        for col in sorted_cols:
            for row in grid:
                result += row[col]
        return result

    @staticmethod
    def column_transposition_encrypt(plaintext, key):
        cols = len(key)
        rows = (len(plaintext) + cols - 1) // cols
        plaintext = plaintext.ljust(rows * cols, 'X')
        grid = [[''] * cols for _ in range(rows)]
        for i, char in enumerate(plaintext):
            grid[i // cols][i % cols] = char
        sorted_cols = sorted(range(cols), key=lambda x: key[x])
        result = ""
        for col in sorted_cols:
            for row in range(rows):
                result += grid[row][col]
        return result

    @staticmethod
    def double_transposition_col_then_row_encrypt(plaintext, key1, key2):
        temp = SymmetricCiphers.column_transposition_encrypt(plaintext, key1)
        return SymmetricCiphers.row_transposition_encrypt(temp, key2)

    @staticmethod
    def double_transposition_row_then_col_encrypt(plaintext, key1, key2):
        temp = SymmetricCiphers.row_transposition_encrypt(plaintext, key1)
        return SymmetricCiphers.column_transposition_encrypt(temp, key2)

    # Modern Block Ciphers
    @staticmethod
    def des_encrypt(plaintext, key):
        key = key[:8].ljust(8, b'\0')[:8]
        cipher = DES.new(key, DES.MODE_ECB)
        plaintext_bytes = plaintext.encode()
        padded = pad(plaintext_bytes, DES.block_size)
        return CryptoUtils.encode_base64(cipher.encrypt(padded))

    @staticmethod
    def double_des_encrypt(plaintext, key1, key2):
        # Encrypt with key1, then encrypt again with key2
        key1 = key1[:8].ljust(8, b'\0')[:8]
        key2 = key2[:8].ljust(8, b'\0')[:8]
        cipher1 = DES.new(key1, DES.MODE_ECB)
        cipher2 = DES.new(key2, DES.MODE_ECB)
        plaintext_bytes = plaintext.encode()
        padded = pad(plaintext_bytes, DES.block_size)
        temp = cipher1.encrypt(padded)
        return CryptoUtils.encode_base64(cipher2.encrypt(temp))

    @staticmethod
    def triple_des_encrypt(plaintext, key):
        key = key[:24].ljust(24, b'\0')[:24]
        cipher = DES3.new(key, DES3.MODE_ECB)
        plaintext_bytes = plaintext.encode()
        padded = pad(plaintext_bytes, DES3.block_size)
        return CryptoUtils.encode_base64(cipher.encrypt(padded))

    @staticmethod
    def aes_encrypt(plaintext, key, mode='ECB'):
        # Ensure key length matches AES requirements (16, 24, or 32 bytes)
        if len(key) not in [16, 24, 32]:
            key = key[:16].ljust(16, b'\0')[:16]

        plaintext_bytes = plaintext.encode()

        if mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            ciphertext = cipher.encrypt(pad(plaintext_bytes, AES.block_size))
        elif mode == 'CBC':
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            ciphertext = iv + cipher.encrypt(pad(plaintext_bytes, AES.block_size))
        elif mode == 'CFB':
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            ciphertext = iv + cipher.encrypt(plaintext_bytes)
        elif mode == 'OFB':
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key, AES.MODE_OFB, iv)
            ciphertext = iv + cipher.encrypt(plaintext_bytes)
        elif mode == 'CTR':
            from Crypto.Util import Counter
            counter = Counter.new(128)
            cipher = AES.new(key, AES.MODE_CTR, counter=counter)
            ciphertext = cipher.encrypt(plaintext_bytes)
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        return CryptoUtils.encode_base64(ciphertext)


# ==================== Asymmetric Ciphers ====================
class AsymmetricCiphers:
    @staticmethod
    def rsa_generate_keys(key_size=2048):
        key = RSA.generate(key_size)
        return key.publickey(), key

    @staticmethod
    def rsa_encrypt(plaintext, public_key):
        cipher = PKCS1_OAEP.new(public_key)
        return CryptoUtils.encode_base64(cipher.encrypt(plaintext.encode()))

    @staticmethod
    def rabin_generate_keys(key_size=1024):
        half_size = key_size // 2
        p = sympy.nextprime(secrets.randbits(half_size))
        while p % 4 != 3:
            p = sympy.nextprime(p)
        q = sympy.nextprime(secrets.randbits(half_size))
        while q % 4 != 3 or q == p:
            q = sympy.nextprime(q)
        n = p * q
        return {'n': n}, {'n': n, 'p': p, 'q': q}

    @staticmethod
    def rabin_encrypt(plaintext, public_key):
        m = int.from_bytes(plaintext.encode(), 'big') % public_key['n']
        c = (m * m) % public_key['n']
        return CryptoUtils.encode_base64(c.to_bytes((public_key['n'].bit_length() + 7) // 8, 'big'))

    @staticmethod
    def ecc_generate_keys():
        key = ECC.generate(curve='P-256')
        return key.public_key(), key

    @staticmethod
    def ecc_encrypt(plaintext, public_key):
        # Simplified ECC encryption using point multiplication
        aes_key = hashlib.sha256(str(public_key.pointQ).encode()).digest()[:16]
        cipher = AES.new(aes_key, AES.MODE_CBC)
        iv = get_random_bytes(AES.block_size)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return CryptoUtils.encode_base64(iv + ciphertext)

    @staticmethod
    def elgamal_generate_keys(key_size=1024):
        p = sympy.nextprime(2 ** key_size)
        g = 2
        while not sympy.is_primitive_root(g, p):
            g += 1
        x = secrets.randbelow(p - 2) + 1
        y = pow(g, x, p)
        return {'p': p, 'g': g, 'y': y}, {'p': p, 'g': g, 'x': x, 'y': y}

    @staticmethod
    def elgamal_encrypt(plaintext, public_key):
        m = int.from_bytes(plaintext.encode(), 'big') % public_key['p']
        k = secrets.randbelow(public_key['p'] - 2) + 1
        c1 = pow(public_key['g'], k, public_key['p'])
        c2 = (m * pow(public_key['y'], k, public_key['p'])) % public_key['p']
        return CryptoUtils.encode_base64(f"{c1},{c2}".encode())

    @staticmethod
    def diffie_hellman_generate_keys(p=None, g=None):
        if p is None:
            p = 23  # Small prime for testing
        if g is None:
            g = 5
        private_key = secrets.randbelow(p - 2) + 1
        public_key = pow(g, private_key, p)
        return {'p': p, 'g': g, 'public': public_key}, private_key

    @staticmethod
    def diffie_hellman_shared_secret(peer_public, private_key, p):
        return pow(peer_public, private_key, p)


# ==================== Digital Signatures ====================
class DigitalSignatures:
    @staticmethod
    def rsa_sign(message, private_key):
        h = SHA256.new(message.encode())
        return CryptoUtils.encode_base64(pkcs1_15.new(private_key).sign(h))

    @staticmethod
    def elgamal_sign(message, private_key):
        p = private_key['p']
        m = int.from_bytes(message.encode(), 'big') % (p - 1)
        k = secrets.randbelow(p - 2) + 1
        while sympy.gcd(k, p - 1) != 1:
            k = secrets.randbelow(p - 2) + 1
        r = pow(private_key['g'], k, p)
        k_inv = pow(k, -1, p - 1)
        s = (k_inv * (m - private_key['x'] * r)) % (p - 1)
        return CryptoUtils.encode_base64(f"{r},{s}".encode())

    @staticmethod
    def schnorr_sign(message, private_key_val, p, g):
        m = int.from_bytes(message.encode(), 'big') % (p - 1)
        k = secrets.randbelow(p - 2) + 1
        r = pow(g, k, p)
        e = int.from_bytes(hashlib.sha256(f"{r}{m}".encode()).digest(), 'big') % (p - 1)
        s = (k + e * private_key_val) % (p - 1)
        return CryptoUtils.encode_base64(f"{e},{s}".encode())

    @staticmethod
    def dh_sign(message, private_key_val, p, g):
        return DigitalSignatures.schnorr_sign(message, private_key_val, p, g)


# ==================== Homomorphic Encryption ====================
class HomomorphicEncryption:
    @staticmethod
    def paillier_generate_keys(key_size=512):
        half_size = key_size // 2
        p = sympy.nextprime(secrets.randbits(half_size))
        q = sympy.nextprime(secrets.randbits(half_size))
        while p == q:
            q = sympy.nextprime(secrets.randbits(half_size))
        n = p * q
        n_sq = n * n
        lambda_n = sympy.lcm(p - 1, q - 1)
        g = n + 1

        def L(u, n):
            return (u - 1) // n

        g_lambda = pow(g, int(lambda_n), n_sq)
        mu = pow(L(g_lambda, n), -1, n)

        return {'n': n, 'g': g, 'n_sq': n_sq}, {'n': n, 'g': g, 'n_sq': n_sq, 'lambda': lambda_n, 'mu': mu}

    @staticmethod
    def paillier_encrypt(plaintext, public_key):
        m = int(plaintext) % public_key['n']
        r = secrets.randbelow(public_key['n'])
        c = (pow(public_key['g'], m, public_key['n_sq']) * pow(r, public_key['n'], public_key['n_sq'])) % public_key[
            'n_sq']
        return c

    @staticmethod
    def paillier_homomorphic_add(c1, c2, public_key):
        return (c1 * c2) % public_key['n_sq']

    @staticmethod
    def elgamal_exp_encrypt(plaintext, public_key):
        m = int(plaintext) % (public_key['p'] - 1)
        k = secrets.randbelow(public_key['p'] - 2) + 1
        c1 = pow(public_key['g'], k, public_key['p'])
        c2 = (pow(public_key['g'], m, public_key['p']) * pow(public_key['y'], k, public_key['p'])) % public_key['p']
        return (c1, c2)

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
def e_build_index(data_dict):
    index = {}
    for user_id, data in data_dict.items():
        for word in data.lower().split():
            word = word.strip('.,!?;:"')
            if word:
                if word not in index:
                    index[word] = set()
                index[word].add(user_id)
    return {k: list(v) for k, v in index.items()}

def e_search2(keyword, index):
    return index.get(keyword.lower().strip('.,!?;:"'), [])



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

def sse_create_index(documents, key):
    index = {}
    for doc_id, doc in documents.items():
        for word in doc.split():
            word_hash = hashlib.sha256(word.encode()).digest()
            if word_hash not in index:
                index[word_hash] = []
            index[word_hash].append(doc_id)
    encrypted_index = {}
    for word_hash, doc_ids in index.items():
        encrypted_index[sse_encrypt_data(key, str(word_hash))[1]] = [sse_encrypt_data(key, str(doc_id))[1]  for doc_id in doc_ids]
    return encrypted_index

def sse_search(encrypted_index, query, key):
    query_hash = hashlib.sha256(query.encode()).digest()
    encrypted_query_hash = sse_encrypt_data(key, str(query_hash))[1]
    if encrypted_query_hash in encrypted_index:
        return [sse_decrypt_data(key, *sse_encrypt_data(key, str(doc_id)))[0] for doc_id in encrypted_index[encrypted_query_hash]]
    else:
        return []

    # @staticmethod
    # def pkse_generate_trapdoor(keyword, key):
    #     return hashlib.sha256(f"{keyword.lower()}{key}".encode()).hexdigest()
    #
    # @staticmethod
    # def nids_encrypt_index(data_dict):
    #     encrypted = {}
    #     for keyword, user_ids in data_dict.items():
    #         keyword_hash = hashlib.sha256(keyword.lower().encode()).hexdigest()
    #         encrypted[keyword_hash] = user_ids
    #     return encrypted
    #
    # @staticmethod
    # def gnupg_encrypt(plaintext, gpg, recipient=None):
    #     try:
    #         if recipient:
    #             encrypted_data = gpg.encrypt(plaintext, recipients=[recipient])
    #         else:
    #             encrypted_data = gpg.encrypt(plaintext, symmetric='AES256')
    #         return str(encrypted_data)
    #     except Exception as e:
    #         return f"GPG_ERROR: {str(e)}"


# ==================== Client Class ====================
class CryptoClient:
    def __init__(self, host=SERVER_HOST, port=SERVER_PORT):
        self.socket = None
        self.host = host
        self.port = port
        self.connected = False

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"[CLIENT] Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"[CLIENT] Connection failed: {e}")
            return False

    def send_message(self, message):
        if not self.connected:
            return False
        try:
            self.socket.sendall((message + "\n").encode('utf-8'))
            return True
        except Exception as e:
            print(f"[CLIENT] Send failed: {e}")
            return False

    def receive_message(self):
        if not self.connected:
            return ""
        try:
            data = self.socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            return data
        except Exception as e:
            print(f"[CLIENT] Receive failed: {e}")
            return ""

    def sending_blank_information(self):
        """Send blank information (Hello message)"""
        self.send_message("HELLO")
        response = self.receive_message()
        print(f"[SERVER] {response}")
        return response

    def test_symmetric_ciphers(self):
        print("\n=== Testing Symmetric Ciphers ===")
        plaintext = "HELLO"

        # Additive Cipher
        encrypted = SymmetricCiphers.additive_cipher_encrypt(plaintext, 3)
        self.send_message(f"SYM:ADDITIVE:{encrypted}")
        print(f"Additive: {encrypted} -> {self.receive_message()}")

        # Vigenere
        encrypted = SymmetricCiphers.vigenere_encrypt(plaintext, "KEY")
        self.send_message(f"SYM:VIGENERE:{encrypted}")
        print(f"Vigenere: {encrypted} -> {self.receive_message()}")

        # DES
        key = b'12345678'
        encrypted = SymmetricCiphers.des_encrypt(plaintext, key)
        self.send_message(f"SYM:DES:{encrypted}")
        print(f"DES: {encrypted[:50]}... -> {self.receive_message()}")

        # AES-128 ECB
        key = b'1234567890123456'
        encrypted = SymmetricCiphers.aes_encrypt(plaintext, key, 'ECB')
        self.send_message(f"SYM:AES128:ECB:{encrypted}")
        print(f"AES-128 ECB: {encrypted[:50]}... -> {self.receive_message()}")

    def test_asymmetric_ciphers(self):
        print("\n=== Testing Asymmetric Ciphers ===")
        plaintext = "SECRET"

        # RSA
        pub, priv = AsymmetricCiphers.rsa_generate_keys(1024)
        encrypted = AsymmetricCiphers.rsa_encrypt(plaintext, pub)
        self.send_message(f"ASYM:RSA:{encrypted}")
        print(f"RSA: {encrypted[:50]}... -> {self.receive_message()}")

        # El Gamal
        pub, priv = AsymmetricCiphers.elgamal_generate_keys(512)
        encrypted = AsymmetricCiphers.elgamal_encrypt(plaintext, pub)
        self.send_message(f"ASYM:ELGAMAL:{encrypted}")
        print(f"El Gamal: {encrypted[:50]}... -> {self.receive_message()}")

    def test_hash_functions(self):
        print("\n=== Testing Hash Functions ===")
        data = "test data"

        hashes = {
            'MD5': HashFunctions.md5_hash(data),
            'SHA1': HashFunctions.sha1_hash(data),
            'SHA256': HashFunctions.sha256_hash(data),
            'SHA512': HashFunctions.sha512_hash(data),
            'SIMPLE': HashFunctions.simple_hash_function(data)
        }

        for name, hash_val in hashes.items():
            self.send_message(f"HASH:{name}:{hash_val}")
            print(f"{name}: {hash_val[:50]}... -> {self.receive_message()}")

    def test_digital_signatures(self):
        print("\n=== Testing Digital Signatures ===")
        message = "Important message"

        # RSA Signature
        pub, priv = AsymmetricCiphers.rsa_generate_keys(1024)
        signature = DigitalSignatures.rsa_sign(message, priv)
        self.send_message(f"SIGN:RSA:{signature}")
        print(f"RSA Signature: {signature[:50]}... -> {self.receive_message()}")

    def test_homomorphic_encryption(self):
        print("\n=== Testing Homomorphic Encryption ===")

        # Paillier Addition
        pub, priv = HomomorphicEncryption.paillier_generate_keys()
        c1 = HomomorphicEncryption.paillier_encrypt(5, pub)
        c2 = HomomorphicEncryption.paillier_encrypt(3, pub)
        c_sum = HomomorphicEncryption.paillier_homomorphic_add(c1, c2, pub)
        self.send_message(f"HOMO:PAILLIER_ADD:{c_sum}")
        print(f"Paillier Add: E(5)+E(3) -> {self.receive_message()}")

        # El Gamal Multiplication
        pub, priv = AsymmetricCiphers.elgamal_generate_keys(512)
        c1 = AsymmetricCiphers.elgamal_encrypt("5", pub)
        c2 = AsymmetricCiphers.elgamal_encrypt("3", pub)
        self.send_message(f"HOMO:ELGAMAL_MULT:{c1},{c2}")
        print(f"El Gamal Mult: E(5)*E(3) -> {self.receive_message()}")

    # def test_searchable_encryption(self):
    #     print("\n=== Testing Searchable Encryption ===")
    #
    #     # SSE
    #     data = {'user1': 'hello world', 'user2': 'hello there'}
    #     index = e_get_index(data)
    #     results = sse_search('hello', index)
    #     self.send_message(f"SEARCH:SSE:hello:{results}")
    #     print(f"SSE Search 'hello': {results} -> {self.receive_message()}")
    #
    #     # PKSE Trapdoor
    #     trapdoor = pkse_generate_trapdoor('secret', 'mykey')
    #     self.send_message(f"SEARCH:PKSE:{trapdoor}")
    #     print(f"PKSE Trapdoor: {trapdoor[:50]}... -> {self.receive_message()}")

    def run_all_tests(self):
        if not self.connect():
            return
        query = 'Diabetes'
        data = {
            'Patient 1': 'D1 Good Diabetes',
            'Patient 2': 'D2 Bad Hypertension',
            'Patient 3': 'D3 Good MRI',
            'Patient 4': 'D4 Bad Cardiology'
        }
        id = e_build_index(data)
        res = e_search2(query, id)
        print('Hospital Connected')
        print('Calculating LeetCode Local Affine')
        affine_ct = SymmetricCiphers.affine_cipher_encrypt(data['Patient 1'], 7, 3)
        print(f'Encrypted: {affine_ct}')
        print('Verification after decryption:', data['Patient 1'] == SymmetricCiphers.affine_cipher_decrypt(affine_ct, 7, 3))
        pub, priv = AsymmetricCiphers.rsa_generate_keys(1024)
        signature = DigitalSignatures.rsa_sign(str(data), priv)
        self.send_message(f"SIGN:RSA:{signature}")
        print(f"RSA Signature: {signature} -> {self.receive_message()}")
        key = get_random_bytes(16)
        hs = HashFunctions.sha512_hash(str(data))
        self.send_message(f"HASH:SHA512:{hs}")
        print(f"Hashing using SHA512 -> {self.receive_message()}")
        index = sse_create_index(data, key)
        results = sse_search(index, query, key)
        self.send_message(f"SEARCH:SSE:MRI:{results}")
        print(res)
        self.socket.close()


if __name__ == "__main__":
    client = CryptoClient()
    client.run_all_tests()
