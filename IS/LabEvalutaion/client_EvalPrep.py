# client.py - Client-side digital signature generation and hash computation

import socket
import json
import hashlib
import random
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class CryptoClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
    
    def send_request(self, request):
        """Send request to server and receive response"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            # Send request
            client_socket.send(json.dumps(request).encode())
            
            # Receive response
            response = client_socket.recv(8192)
            client_socket.close()
            
            return json.loads(response.decode())
        except Exception as e:
            return {'status': 'error', 'message': f'Connection error: {str(e)}'}
    
    def test_rsa_signature(self, message):
        """Generate and verify RSA signature"""
        print("\n[*] Testing RSA Digital Signature")
        print(f"Message: {message}")
        
        # Generate RSA key pair
        key = RSA.generate(2048)
        public_key = key.publickey()
        
        # Sign message
        h = SHA256.new(message.encode())
        signature = pkcs1_15.new(key).sign(h)
        
        # Prepare request
        request = {
            'type': 'RSA',
            'message': message,
            'signature': signature.hex(),
            'public_key': public_key.export_key().decode()
        }
        
        # Send to server for verification
        response = self.send_request(request)
        print(f"Server Response: {response}")
        return response
    
    def test_rabin_signature(self, message):
        """Generate and verify Rabin signature"""
        print("\n[*] Testing Rabin Digital Signature")
        print(f"Message: {message}")
        
        # Generate Rabin parameters (two primes p and q where p ≡ q ≡ 3 (mod 4))
        p = 499  # prime ≡ 3 (mod 4)
        q = 547  # prime ≡ 3 (mod 4)
        n = p * q
        
        # Private key: (p, q), Public key: n
        message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16) % n
        
        # Sign: compute square root of message_hash mod n
        # Simplified for demonstration
        signature = pow(message_hash, (p + 1) // 4, p)  # Simplified signing
        
        # Prepare request
        request = {
            'type': 'Rabin',
            'message': message,
            'signature': signature,
            'n': n
        }
        
        # Send to server for verification
        response = self.send_request(request)
        print(f"Server Response: {response}")
        return response
    
    def test_diffie_hellman(self):
        """Perform Diffie-Hellman key exchange"""
        print("\n[*] Testing Diffie-Hellman Key Exchange")
        
        # DH parameters
        p = 23  # prime (use larger prime in production)
        g = 5   # generator
        
        # Client's private key
        client_private = random.randint(2, p - 2)
        
        # Client's public value: g^a mod p
        client_public = pow(g, client_private, p)
        
        print(f"Client Private Key: {client_private}")
        print(f"Client Public Value: {client_public}")
        
        # Prepare request
        request = {
            'type': 'DH',
            'client_public': client_public,
            'p': p,
            'g': g
        }
        
        # Send to server
        response = self.send_request(request)
        
        if response['status'] == 'success':
            server_public = response['server_public']
            # Compute client's shared secret
            client_shared_secret = pow(server_public, client_private, p)
            
            print(f"Server Public Value: {server_public}")
            print(f"Client Computed Shared Secret: {client_shared_secret}")
            print(f"Server Computed Shared Secret: {response['shared_secret']}")
            print(f"Secrets Match: {client_shared_secret == response['shared_secret']}")
        
        return response
    
    def test_elgamal_signature(self, message):
        """Generate and verify ElGamal signature"""
        print("\n[*] Testing ElGamal Digital Signature")
        print(f"Message: {message}")
        
        # ElGamal parameters
        p = 23  # prime (use larger prime in production)
        g = 5   # generator
        
        # Private key
        x = random.randint(2, p - 2)
        
        # Public key: y = g^x mod p
        y = pow(g, x, p)
        
        # Sign message
        k = random.randint(2, p - 2)
        while self.gcd(k, p - 1) != 1:
            k = random.randint(2, p - 2)
        
        r = pow(g, k, p)
        message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16) % (p - 1)
        
        k_inv = self.mod_inverse(k, p - 1)
        s = (k_inv * (message_hash - x * r)) % (p - 1)
        
        # Prepare request
        request = {
            'type': 'ElGamal',
            'message': message,
            'r': r,
            's': s,
            'p': p,
            'g': g,
            'y': y
        }
        
        # Send to server for verification
        response = self.send_request(request)
        print(f"Server Response: {response}")
        return response
    
    def test_schnorr_signature(self, message):
        """Generate and verify Schnorr signature"""
        print("\n[*] Testing Schnorr Digital Signature")
        print(f"Message: {message}")
        
        # Schnorr parameters
        p = 23  # prime (use larger prime in production)
        q = 11  # prime divisor of p-1
        g = 2   # generator of order q
        
        # Private key
        x = random.randint(1, q - 1)
        
        # Public key: y = g^(-x) mod p
        y = pow(g, -x, p)
        
        # Sign message
        k = random.randint(1, q - 1)
        r = pow(g, k, p)
        
        e = int(hashlib.sha256((message + str(r)).encode()).hexdigest(), 16) % q
        s = (k + x * e) % q
        
        # Prepare request
        request = {
            'type': 'Schnorr',
            'message': message,
            'r': r,
            's': s,
            'p': p,
            'q': q,
            'g': g,
            'y': y
        }
        
        # Send to server for verification
        response = self.send_request(request)
        print(f"Server Response: {response}")
        return response
    
    def test_hash_verification(self, message):
        """Test hash verification for multiple hash algorithms"""
        print("\n[*] Testing Hash Verification")
        print(f"Message: {message}")
        
        hash_algorithms = ['MD5', 'SHA1', 'SHA256', 'SHA512']
        
        for hash_type in hash_algorithms:
            # Compute hash
            if hash_type == 'MD5':
                hash_value = hashlib.md5(message.encode()).hexdigest()
            elif hash_type == 'SHA1':
                hash_value = hashlib.sha1(message.encode()).hexdigest()
            elif hash_type == 'SHA256':
                hash_value = hashlib.sha256(message.encode()).hexdigest()
            elif hash_type == 'SHA512':
                hash_value = hashlib.sha512(message.encode()).hexdigest()
            
            print(f"\n{hash_type} Hash: {hash_value}")
            
            # Prepare request
            request = {
                'type': 'HASH',
                'message': message,
                'hash_type': hash_type,
                'hash_value': hash_value
            }
            
            # Send to server for verification
            response = self.send_request(request)
            print(f"Server Response: {response}")
    
    @staticmethod
    def gcd(a, b):
        """Compute greatest common divisor"""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def mod_inverse(a, m):
        """Compute modular multiplicative inverse"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise Exception('Modular inverse does not exist')
        return (x % m + m) % m
    
    def run_all_tests(self):
        """Run all cryptographic tests"""
        message = "This is a test message for cryptographic verification"
        
        print("="*70)
        print("CRYPTOGRAPHIC SIGNATURE AND HASH VERIFICATION TESTS")
        print("="*70)
        
        # Test all signature schemes
        self.test_rsa_signature(message)
        self.test_rabin_signature(message)
        self.test_diffie_hellman()
        self.test_elgamal_signature(message)
        self.test_schnorr_signature(message)
        
        # Test hash verification
        self.test_hash_verification(message)
        
        print("\n" + "="*70)
        print("ALL TESTS COMPLETED")
        print("="*70)

if __name__ == "__main__":
    client = CryptoClient()
    client.run_all_tests()
