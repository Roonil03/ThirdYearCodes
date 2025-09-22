# requirements: pip install pycryptodome sympy numpy

import hashlib
import string
import numpy as np
from sympy import mod_inverse, isprime, nextprime
import math
import random
from Crypto.Cipher import DES, AES
from Crypto.PublicKey import RSA, ECC
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util import number
from Crypto.PublicKey import ElGamal
from Crypto.Protocol.KDF import PBKDF2

class ClassicalCiphers:
    """Implementation of classical encryption algorithms"""
    
    @staticmethod
    def additive_encrypt(plaintext, key):
        """Caesar/Additive cipher encryption"""
        result = ""
        for char in plaintext.upper():
            if char.isalpha():
                shifted = (ord(char) - ord('A') + key) % 26
                result += chr(shifted + ord('A'))
            else:
                result += char
        return result
    
    @staticmethod
    def additive_decrypt(ciphertext, key):
        """Caesar/Additive cipher decryption"""
        return ClassicalCiphers.additive_encrypt(ciphertext, -key)
    
    @staticmethod
    def multiplicative_encrypt(plaintext, key):
        """Multiplicative cipher encryption"""
        if math.gcd(key, 26) != 1:
            raise ValueError("Key must be coprime with 26")
        
        result = ""
        for char in plaintext.upper():
            if char.isalpha():
                encrypted = ((ord(char) - ord('A')) * key) % 26
                result += chr(encrypted + ord('A'))
            else:
                result += char
        return result
    
    @staticmethod
    def multiplicative_decrypt(ciphertext, key):
        """Multiplicative cipher decryption"""
        if math.gcd(key, 26) != 1:
            raise ValueError("Key must be coprime with 26")
        
        key_inv = mod_inverse(key, 26)
        result = ""
        for char in ciphertext.upper():
            if char.isalpha():
                decrypted = ((ord(char) - ord('A')) * key_inv) % 26
                result += chr(decrypted + ord('A'))
            else:
                result += char
        return result
    
    @staticmethod
    def affine_encrypt(plaintext, a, b):
        """Affine cipher encryption: C = (a*P + b) mod 26"""
        if math.gcd(a, 26) != 1:
            raise ValueError("'a' must be coprime with 26")
        
        result = ""
        for char in plaintext.upper():
            if char.isalpha():
                encrypted = (a * (ord(char) - ord('A')) + b) % 26
                result += chr(encrypted + ord('A'))
            else:
                result += char
        return result
    
    @staticmethod
    def affine_decrypt(ciphertext, a, b):
        """Affine cipher decryption: P = a^-1 * (C - b) mod 26"""
        if math.gcd(a, 26) != 1:
            raise ValueError("'a' must be coprime with 26")
        
        a_inv = mod_inverse(a, 26)
        result = ""
        for char in ciphertext.upper():
            if char.isalpha():
                decrypted = (a_inv * (ord(char) - ord('A') - b)) % 26
                result += chr(decrypted + ord('A'))
            else:
                result += char
        return result
    
    @staticmethod
    def vigenere_encrypt(plaintext, key):
        """Vigenère cipher encryption"""
        result = ""
        key = key.upper()
        key_index = 0
        
        for char in plaintext.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                encrypted = (ord(char) - ord('A') + shift) % 26
                result += chr(encrypted + ord('A'))
                key_index += 1
            else:
                result += char
        return result
    
    @staticmethod
    def vigenere_decrypt(ciphertext, key):
        """Vigenère cipher decryption"""
        result = ""
        key = key.upper()
        key_index = 0
        
        for char in ciphertext.upper():
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('A')
                decrypted = (ord(char) - ord('A') - shift) % 26
                result += chr(decrypted + ord('A'))
                key_index += 1
            else:
                result += char
        return result
    
    @staticmethod
    def autokey_encrypt(plaintext, key):
        """Autokey cipher encryption"""
        plaintext = plaintext.upper().replace(' ', '')
        key = key.upper()
        
        # Extend key with plaintext
        full_key = key + plaintext
        result = ""
        
        for i, char in enumerate(plaintext):
            if char.isalpha():
                shift = ord(full_key[i]) - ord('A')
                encrypted = (ord(char) - ord('A') + shift) % 26
                result += chr(encrypted + ord('A'))
        return result
    
    @staticmethod
    def autokey_decrypt(ciphertext, key):
        """Autokey cipher decryption"""
        key = key.upper()
        result = ""
        full_key = key
        
        for i, char in enumerate(ciphertext.upper()):
            if char.isalpha():
                shift = ord(full_key[i]) - ord('A')
                decrypted = (ord(char) - ord('A') - shift) % 26
                decrypted_char = chr(decrypted + ord('A'))
                result += decrypted_char
                full_key += decrypted_char
        return result
    
    @staticmethod
    def playfair_create_matrix(key):
        """Create 5x5 Playfair matrix"""
        key = key.upper().replace('J', 'I')
        alphabet = string.ascii_uppercase.replace('J', '')
        
        # Remove duplicates from key
        seen = set()
        matrix_chars = []
        for char in key + alphabet:
            if char not in seen and char.isalpha():
                seen.add(char)
                matrix_chars.append(char)
        
        return [matrix_chars[i*5:(i+1)*5] for i in range(5)]
    
    @staticmethod
    def playfair_find_position(char, matrix):
        """Find position of character in matrix"""
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j
        return None
    
    @staticmethod
    def playfair_encrypt(plaintext, key):
        """Playfair cipher encryption"""
        matrix = ClassicalCiphers.playfair_create_matrix(key)
        plaintext = plaintext.upper().replace('J', 'I').replace(' ', '')
        
        # Create pairs
        pairs = []
        i = 0
        while i < len(plaintext):
            if i == len(plaintext) - 1:
                pairs.append(plaintext[i] + 'X')
                break
            elif plaintext[i] == plaintext[i + 1]:
                pairs.append(plaintext[i] + 'X')
                i += 1
            else:
                pairs.append(plaintext[i:i+2])
                i += 2
        
        result = ""
        for pair in pairs:
            row1, col1 = ClassicalCiphers.playfair_find_position(pair[0], matrix)
            row2, col2 = ClassicalCiphers.playfair_find_position(pair[1], matrix)
            
            if row1 == row2:  # Same row
                result += matrix[row1][(col1 + 1) % 5]
                result += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Same column
                result += matrix[(row1 + 1) % 5][col1]
                result += matrix[(row2 + 1) % 5][col2]
            else:  # Rectangle
                result += matrix[row1][col2]
                result += matrix[row2][col1]
        
        return result
    
    @staticmethod
    def playfair_decrypt(ciphertext, key):
        """Playfair cipher decryption"""
        matrix = ClassicalCiphers.playfair_create_matrix(key)
        pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        
        result = ""
        for pair in pairs:
            row1, col1 = ClassicalCiphers.playfair_find_position(pair[0], matrix)
            row2, col2 = ClassicalCiphers.playfair_find_position(pair[1], matrix)
            
            if row1 == row2:  # Same row
                result += matrix[row1][(col1 - 1) % 5]
                result += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Same column
                result += matrix[(row1 - 1) % 5][col1]
                result += matrix[(row2 - 1) % 5][col2]
            else:  # Rectangle
                result += matrix[row1][col2]
                result += matrix[row2][col1]
        
        return result
    
    @staticmethod
    def hill_cipher_encrypt(plaintext, key_matrix):
        """Hill cipher encryption"""
        plaintext = plaintext.upper().replace(' ', '')
        n = key_matrix.shape[0]
        
        # Pad message if needed
        while len(plaintext) % n != 0:
            plaintext += 'X'
        
        result = ""
        for i in range(0, len(plaintext), n):
            block = plaintext[i:i+n]
            vector = np.array([[ord(char) - ord('A')] for char in block])
            encrypted_vector = (key_matrix @ vector) % 26
            result += ''.join([chr(int(val[0]) + ord('A')) for val in encrypted_vector])
        
        return result
    
    @staticmethod
    def railfence_encrypt(plaintext, rails):
        """Rail fence cipher encryption"""
        if rails == 1:
            return plaintext
        
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for char in plaintext:
            fence[rail].append(char)
            rail += direction
            
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        return ''.join([''.join(row) for row in fence])
    
    @staticmethod
    def railfence_decrypt(ciphertext, rails):
        """Rail fence cipher decryption"""
        if rails == 1:
            return ciphertext
        
        # Calculate lengths of each rail
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for i in range(len(ciphertext)):
            fence[rail].append(0)
            rail += direction
            
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        # Fill fence with ciphertext
        index = 0
        for i in range(rails):
            for j in range(len(fence[i])):
                fence[i][j] = ciphertext[index]
                index += 1
        
        # Read in zigzag pattern
        result = ""
        rail = 0
        direction = 1
        for i in range(len(ciphertext)):
            result += fence[rail].pop(0)
            rail += direction
            
            if rail == rails - 1 or rail == 0:
                direction = -direction
        
        return result
    
    @staticmethod
    def keyed_transposition_encrypt(plaintext, key):
        """Keyed transposition cipher encryption"""
        # Create column order based on key
        key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
        col_order = [x[0] for x in key_order]
        
        rows = math.ceil(len(plaintext) / len(key))
        grid = []
        
        # Fill grid row by row
        for i in range(rows):
            row = []
            for j in range(len(key)):
                if i * len(key) + j < len(plaintext):
                    row.append(plaintext[i * len(key) + j])
                else:
                    row.append('')
            grid.append(row)
        
        # Read columns in key order
        result = ""
        for col_idx in col_order:
            for row in grid:
                if col_idx < len(row) and row[col_idx]:
                    result += row[col_idx]
        
        return result
    
    @staticmethod
    def keyed_transposition_decrypt(ciphertext, key):
        """Keyed transposition cipher decryption"""
        key_order = sorted(list(enumerate(key)), key=lambda x: x[1])
        col_order = [x[0] for x in key_order]
        
        rows = math.ceil(len(ciphertext) / len(key))
        cols = len(key)
        
        # Calculate column lengths
        col_lengths = [rows] * cols
        remaining = len(ciphertext) % cols
        if remaining:
            for i in range(cols - remaining):
                col_lengths[col_order[cols - 1 - i]] -= 1
        
        # Fill columns
        grid = [['' for _ in range(cols)] for _ in range(rows)]
        idx = 0
        for i, col_idx in enumerate(col_order):
            for row in range(col_lengths[col_idx]):
                if idx < len(ciphertext):
                    grid[row][col_idx] = ciphertext[idx]
                    idx += 1
        
        # Read row by row
        result = ""
        for row in grid:
            result += ''.join(row)
        
        return result.rstrip()

class SymmetricCiphers:
    """Implementation of symmetric encryption algorithms"""
    
    @staticmethod
    def pad_data(data, block_size):
        """PKCS7 padding"""
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    @staticmethod
    def unpad_data(data):
        """Remove PKCS7 padding"""
        padding_length = data[-1]
        return data[:-padding_length]
    
    @staticmethod
    def des_encrypt(plaintext, key):
        """DES encryption"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        if isinstance(key, str):
            key = key.encode()
        
        # Ensure key is 8 bytes
        key = key[:8].ljust(8, b'\x00')
        
        # Pad plaintext
        plaintext = SymmetricCiphers.pad_data(plaintext, 8)
        
        cipher = DES.new(key, DES.MODE_ECB)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def des_decrypt(ciphertext, key):
        """DES decryption"""
        if isinstance(key, str):
            key = key.encode()
        
        # Ensure key is 8 bytes
        key = key[:8].ljust(8, b'\x00')
        
        cipher = DES.new(key, DES.MODE_ECB)
        decrypted = cipher.decrypt(ciphertext)
        return SymmetricCiphers.unpad_data(decrypted)
    
    @staticmethod
    def triple_des_encrypt(plaintext, key):
        """Triple DES encryption"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        if isinstance(key, str):
            key = key.encode()
        
        # Ensure key is 24 bytes (or adjust to 16/24)
        if len(key) <= 16:
            key = key[:16].ljust(16, b'\x00')
        else:
            key = key[:24].ljust(24, b'\x00')
        
        plaintext = SymmetricCiphers.pad_data(plaintext, 8)
        
        cipher = DES3.new(key, DES3.MODE_ECB)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def triple_des_decrypt(ciphertext, key):
        """Triple DES decryption"""
        if isinstance(key, str):
            key = key.encode()
        
        if len(key) <= 16:
            key = key[:16].ljust(16, b'\x00')
        else:
            key = key[:24].ljust(24, b'\x00')
        
        cipher = DES3.new(key, DES3.MODE_ECB)
        decrypted = cipher.decrypt(ciphertext)
        return SymmetricCiphers.unpad_data(decrypted)
    
    @staticmethod
    def aes_encrypt(plaintext, key, key_size=128):
        """AES encryption (128, 192, or 256 bit)"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        if isinstance(key, str):
            key = key.encode()
        
        # Adjust key size
        key_bytes = key_size // 8
        key = key[:key_bytes].ljust(key_bytes, b'\x00')
        
        plaintext = SymmetricCiphers.pad_data(plaintext, 16)
        
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def aes_decrypt(ciphertext, key, key_size=128):
        """AES decryption (128, 192, or 256 bit)"""
        if isinstance(key, str):
            key = key.encode()
        
        key_bytes = key_size // 8
        key = key[:key_bytes].ljust(key_bytes, b'\x00')
        
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(ciphertext)
        return SymmetricCiphers.unpad_data(decrypted)

class AsymmetricCiphers:
    """Implementation of asymmetric encryption algorithms"""
    
    @staticmethod
    def rsa_generate_keys(key_size=2048):
        """Generate RSA key pair"""
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
    
    @staticmethod
    def rsa_encrypt(plaintext, public_key_pem):
        """RSA encryption"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
        
        public_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def rsa_decrypt(ciphertext, private_key_pem):
        """RSA decryption"""
        private_key = RSA.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(ciphertext)
    
    @staticmethod
    def elgamal_generate_keys(key_size=2048):
        """Generate ElGamal key pair"""
        key = ElGamal.generate(key_size, get_random_bytes)
        return key
    
    @staticmethod
    def elgamal_encrypt(message, public_key):
        """ElGamal encryption (simplified for small messages)"""
        if isinstance(message, str):
            message = message.encode()
        
        # Convert message to integer
        m = int.from_bytes(message, 'big')
        
        p, g, y = public_key.p, public_key.g, public_key.y
        
        if m >= p:
            raise ValueError("Message too large for key size")
        
        k = number.getRandomRange(2, p-1)
        c1 = pow(g, k, p)
        c2 = (m * pow(y, k, p)) % p
        
        return (c1, c2)
    
    @staticmethod
    def elgamal_decrypt(ciphertext, private_key):
        """ElGamal decryption"""
        c1, c2 = ciphertext
        p, x = private_key.p, private_key.x
        
        s = pow(c1, x, p)
        s_inv = number.inverse(s, p)
        m = (c2 * s_inv) % p
        
        # Convert back to bytes
        byte_length = (m.bit_length() + 7) // 8
        return m.to_bytes(byte_length, 'big')
    
    @staticmethod
    def ecc_generate_keys():
        """Generate ECC key pair"""
        key = ECC.generate(curve='P-256')
        private_key = key.export_key(format='PEM')
        public_key = key.public_key().export_key(format='PEM')
        return private_key, public_key
    
    @staticmethod
    def diffie_hellman_generate_params():
        """Generate Diffie-Hellman parameters"""
        p = number.getPrime(2048)
        g = 2
        return p, g
    
    @staticmethod
    def diffie_hellman_generate_private_key(p):
        """Generate DH private key"""
        return number.getRandomRange(2, p-1)
    
    @staticmethod
    def diffie_hellman_generate_public_key(g, private_key, p):
        """Generate DH public key"""
        return pow(g, private_key, p)
    
    @staticmethod
    def diffie_hellman_shared_secret(other_public_key, private_key, p):
        """Generate shared secret"""
        return pow(other_public_key, private_key, p)
    
    @staticmethod
    def rabin_generate_keys(key_size=1024):
        """Generate Rabin cryptosystem keys"""
        # Generate two large primes p, q ≡ 3 (mod 4)
        while True:
            p = number.getPrime(key_size // 2)
            if p % 4 == 3:
                break
        
        while True:
            q = number.getPrime(key_size // 2)
            if q % 4 == 3 and q != p:
                break
        
        n = p * q
        return (n, p, q)  # (public_key, private_key components)
    
    @staticmethod
    def rabin_encrypt(message, public_key):
        """Rabin encryption"""
        if isinstance(message, str):
            message = message.encode()
        
        m = int.from_bytes(message, 'big')
        n = public_key
        
        if m >= n:
            raise ValueError("Message too large for key size")
        
        return pow(m, 2, n)
    
    @staticmethod
    def rabin_decrypt(ciphertext, private_key):
        """Rabin decryption (returns one of four possible plaintexts)"""
        n, p, q = private_key
        
        # Calculate square roots modulo p and q
        mp = pow(ciphertext, (p + 1) // 4, p)
        mq = pow(ciphertext, (q + 1) // 4, q)
        
        # Use Chinese Remainder Theorem
        yp = number.inverse(p, q)
        yq = number.inverse(q, p)
        
        r1 = (yp * p * mq + yq * q * mp) % n
        r2 = (yp * p * mq - yq * q * mp) % n
        r3 = (-yp * p * mq + yq * q * mp) % n
        r4 = (-yp * p * mq - yq * q * mp) % n
        
        # Return the smallest positive root (heuristic)
        roots = [r1, r2, r3, r4]
        m = min(root % n for root in roots)
        
        byte_length = (m.bit_length() + 7) // 8
        return m.to_bytes(byte_length, 'big')

class HashingAlgorithms:
    """Implementation of hashing algorithms"""
    
    @staticmethod
    def sha256(data):
        """SHA-256 hashing"""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def sha1(data):
        """SHA-1 hashing"""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha1(data).hexdigest()
    
    @staticmethod
    def md5(data):
        """MD5 hashing"""
        if isinstance(data, str):
            data = data.encode()
        return hashlib.md5(data).hexdigest()

# Example usage and testing
if __name__ == "__main__":
    # Example usage of various algorithms
    
    print("=== Classical Ciphers ===")
    
    # Additive/Caesar Cipher
    plaintext = "HELLO WORLD"
    key = 3
    encrypted = ClassicalCiphers.additive_encrypt(plaintext, key)
    decrypted = ClassicalCiphers.additive_decrypt(encrypted, key)
    print(f"Additive Cipher - Original: {plaintext}, Encrypted: {encrypted}, Decrypted: {decrypted}")
    
    # Multiplicative Cipher
    key = 7
    encrypted = ClassicalCiphers.multiplicative_encrypt(plaintext, key)
    decrypted = ClassicalCiphers.multiplicative_decrypt(encrypted, key)
    print(f"Multiplicative Cipher - Original: {plaintext}, Encrypted: {encrypted}, Decrypted: {decrypted}")
    
    # Affine Cipher
    a, b = 5, 8
    encrypted = ClassicalCiphers.affine_encrypt(plaintext, a, b)
    decrypted = ClassicalCiphers.affine_decrypt(encrypted, a, b)
    print(f"Affine Cipher - Original: {plaintext}, Encrypted: {encrypted}, Decrypted: {decrypted}")
    
    # Vigenère Cipher
    key = "KEY"
    encrypted = ClassicalCiphers.vigenere_encrypt(plaintext, key)
    decrypted = ClassicalCiphers.vigenere_decrypt(encrypted, key)
    print(f"Vigenère Cipher - Original: {plaintext}, Encrypted: {encrypted}, Decrypted: {decrypted}")
    
    # Rail Fence Cipher
    rails = 3
    encrypted = ClassicalCiphers.railfence_encrypt(plaintext, rails)
    decrypted = ClassicalCiphers.railfence_decrypt(encrypted, rails)
    print(f"Rail Fence Cipher - Original: {plaintext}, Encrypted: {encrypted}, Decrypted: {decrypted}")
    
    print("\n=== Symmetric Ciphers ===")
    
    # AES-128
    key = "mysecretkey12345"
    encrypted = SymmetricCiphers.aes_encrypt(plaintext, key, 128)
    decrypted = SymmetricCiphers.aes_decrypt(encrypted, key, 128)
    print(f"AES-128 - Original: {plaintext}, Decrypted: {decrypted.decode()}")
    
    print("\n=== Asymmetric Ciphers ===")
    
    # RSA
    private_key, public_key = AsymmetricCiphers.rsa_generate_keys()
    encrypted = AsymmetricCiphers.rsa_encrypt("Hello RSA", public_key)
    decrypted = AsymmetricCiphers.rsa_decrypt(encrypted, private_key)
    print(f"RSA - Decrypted: {decrypted.decode()}")
    
    print("\n=== Hashing ===")
    
    # Hash algorithms
    data = "Hello World"
    print(f"SHA-256: {HashingAlgorithms.sha256(data)}")
    print(f"SHA-1: {HashingAlgorithms.sha1(data)}")
    print(f"MD5: {HashingAlgorithms.md5(data)}")
