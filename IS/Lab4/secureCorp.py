import random
import math
import hashlib
from datetime import datetime, timedelta


class RSASystem:
    def __init__(self, key_size: int = 1024):
        self.key_size = key_size
        self.public_key = None
        self.private_key = None

    def _is_prime(self, n: int) -> bool:
        if n < 2: return False
        if n in (2, 3): return True
        if n % 2 == 0: return False
        r, d = 0, n - 1
        while d % 2 == 0: r, d = r + 1, d // 2
        for _ in range(5):  # Miller-Rabin rounds
            a = random.randrange(2, n - 2)
            x = pow(a, d, n)
            if x in (1, n - 1): continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1: break
            else:
                return False
        return True

    def _generate_prime(self, bits: int) -> int:
        while True:
            p = random.getrandbits(bits)
            p |= (1 << bits - 1) | 1
            if self._is_prime(p): return p

    def _extended_gcd(self, a: int, b: int):
        if a == 0: return b, 0, 1
        gcd, x1, y1 = self._extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    def _mod_inverse(self, e: int, phi: int) -> int:
        gcd, x, _ = self._extended_gcd(e, phi)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return x % phi

    def generate_keypair(self):
        p = self._generate_prime(self.key_size // 2)
        q = self._generate_prime(self.key_size // 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        while math.gcd(e, phi) != 1:
            e += 2
        d = self._mod_inverse(e, phi)
        self.public_key = (n, e)
        self.private_key = (n, d)
        return self.public_key, self.private_key

    def encrypt(self, message: int, public_key) -> int:
        n, e = public_key
        return pow(message, e, n)

    def decrypt(self, ciphertext: int, private_key) -> int:
        n, d = private_key
        return pow(ciphertext, d, n)

class DiffieHellmanSystem:
    def __init__(self):
        self.prime = int(''.join([
            "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1",
            "29024E088A67CC74020BBEA63B139B22514A08798E3404DDEF",
            "9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E48",
            "5B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BF",
            "B5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163",
            "BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961",
            "C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C0",
            "8CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A2",
            "8FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D22",
            "61898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF"
        ]), 16)
        self.generator = 2
        self.private_key = None
        self.public_key = None

    def generate_private_key(self):
        self.private_key = random.randrange(2, self.prime - 1)
        return self.private_key

    def generate_public_key(self, private_key: int):
        self.public_key = pow(self.generator, private_key, self.prime)
        return self.public_key

    def compute_shared_secret(self, other_public_key: int, private_key: int):
        return pow(other_public_key, private_key, self.prime)

class KeyManager:
    def __init__(self):
        self.keys = {}
        self.key_counter = 0
        self.revoked_keys = set()

    def generate_key_id(self):
        self.key_counter += 1
        return f"KEY_{self.key_counter:06d}"

    def store_key(self, key_data, key_type, owner, expiry_hours=24):
        key_id = self.generate_key_id()
        expiry_time = datetime.now() + timedelta(hours=expiry_hours)
        self.keys[key_id] = {
            'key_data': key_data,
            'key_type': key_type,
            'owner': owner,
            'created_at': datetime.now(),
            'expires_at': expiry_time,
            'status': 'active'
        }
        return key_id

    def retrieve_key(self, key_id: str):
        if key_id not in self.keys or key_id in self.revoked_keys:
            return None
        key_info = self.keys[key_id]
        if datetime.now() > key_info['expires_at']:
            key_info['status'] = 'expired'
            return None
        return key_info

    def revoke_key(self, key_id: str):
        if key_id in self.keys:
            self.revoked_keys.add(key_id)
            self.keys[key_id]['status'] = 'revoked'
            return True
        return False

    def list_keys(self, owner=None):
        result = []
        for key_id, key_info in self.keys.items():
            if owner is None or key_info['owner'] == owner:
                result.append({
                    'key_id': key_id,
                    'key_type': key_info['key_type'],
                    'owner': key_info['owner'],
                    'status': key_info['status'],
                    'created_at': key_info['created_at'].isoformat(),
                    'expires_at': key_info['expires_at'].isoformat()
                })
        return result

class SecureSystem:
    def __init__(self, system_name, system_id):
        self.system_name = system_name
        self.system_id = system_id
        self.rsa = RSASystem()
        self.dh = DiffieHellmanSystem()
        self.key_manager = KeyManager()
        self.rsa_public, self.rsa_private = self.rsa.generate_keypair()
        self.rsa_key_id = self.key_manager.store_key(
            {'public_key': self.rsa_public, 'private_key': self.rsa_private},
            'RSA', system_name, expiry_hours=168
        )

    def initiate_dh_exchange(self):
        private_key = self.dh.generate_private_key()
        public_key = self.dh.generate_public_key(private_key)
        dh_key_id = self.key_manager.store_key(
            {'private_key': private_key, 'public_key': public_key,
             'prime': self.dh.prime, 'generator': self.dh.generator},
            'DH', self.system_name, expiry_hours=1
        )
        return {
            'system_id': self.system_id,
            'dh_public_key': public_key,
            'dh_key_id': dh_key_id,
            'prime': self.dh.prime,
            'generator': self.dh.generator
        }

    def complete_dh_exchange(self, other_public_key, dh_key_id):
        dh_key_info = self.key_manager.retrieve_key(dh_key_id)
        if not dh_key_info: return None
        private_key = dh_key_info['key_data']['private_key']
        shared_secret = self.dh.compute_shared_secret(other_public_key, private_key)
        shared_key_id = self.key_manager.store_key(
            {'shared_secret': shared_secret}, 'SHARED_SECRET',
            self.system_name, expiry_hours=1
        )
        return shared_secret

    def encrypt_message(self, message, recipient_public_key):
        message_int = int.from_bytes(message.encode('utf-8'), 'big')
        if message_int >= recipient_public_key[0]:
            message_hash = hashlib.sha256(message.encode()).hexdigest()
            message_int = int(message_hash[:16], 16)
        ciphertext = self.rsa.encrypt(message_int, recipient_public_key)
        return {
            'ciphertext': ciphertext,
            'sender': self.system_id,
            'timestamp': datetime.now().isoformat()
        }

    def decrypt_message(self, encrypted_data):
        ciphertext = encrypted_data['ciphertext']
        decrypted_int = self.rsa.decrypt(ciphertext, self.rsa_private)
        try:
            decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
            return decrypted_bytes.decode('utf-8')
        except:
            return hex(decrypted_int)

class SecureCorpEnterprise:
    def __init__(self):
        self.systems = {}
        self.master_key_manager = KeyManager()

    def register_system(self, system_name, system_id):
        system = SecureSystem(system_name, system_id)
        self.systems[system_id] = system
        self.master_key_manager.store_key(
            {'public_key': system.rsa_public, 'system_id': system_id},
            'SYSTEM_RSA_PUBLIC', 'Enterprise', expiry_hours=8760
        )
        return system

    def facilitate_secure_communication(self, sender_id, receiver_id, message):
        if sender_id not in self.systems or receiver_id not in self.systems:
            return {'success': False, 'error': 'System not found'}
        sender = self.systems[sender_id]
        receiver = self.systems[receiver_id]
        encrypted_data = sender.encrypt_message(message, receiver.rsa_public)
        decrypted_message = receiver.decrypt_message(encrypted_data)
        return {
            'success': True,
            'sender': sender_id,
            'receiver': receiver_id,
            'original_message': message,
            'encrypted_data': encrypted_data,
            'decrypted_message': decrypted_message
        }

    def establish_session_key(self, system1_id, system2_id):
        if system1_id not in self.systems or system2_id not in self.systems:
            return {'success': False, 'error': 'System not found'}
        system1 = self.systems[system1_id]
        system2 = self.systems[system2_id]
        dh_data1 = system1.initiate_dh_exchange()
        dh_data2 = system2.initiate_dh_exchange()
        shared_secret1 = system1.complete_dh_exchange(
            dh_data2['dh_public_key'], dh_data1['dh_key_id'])
        shared_secret2 = system2.complete_dh_exchange(
            dh_data1['dh_public_key'], dh_data2['dh_key_id'])
        return {
            'success': True,
            'system1': system1_id,
            'system2': system2_id,
            'shared_secret_match': shared_secret1 == shared_secret2,
            'shared_secret': shared_secret1,
            'dh_exchange_data': {
                'system1_public': dh_data1['dh_public_key'],
                'system2_public': dh_data2['dh_public_key']
            }
        }


def demonstrate_system():
    print("Initializing SecureCorp Enterprise System...")
    enterprise = SecureCorpEnterprise()
    finance_system = enterprise.register_system("Finance System", "SYS_FINANCE")
    hr_system = enterprise.register_system("HR System", "SYS_HR")
    supply_system = enterprise.register_system("Supply Chain Management", "SYS_SUPPLY")
    print("✓ Finance System registered with ID: SYS_FINANCE")
    print("✓ HR System registered with ID: SYS_HR")
    print("✓ Supply Chain Management registered with ID: SYS_SUPPLY")
    print("\n2. RSA Key Information:")
    for sys_id, system in enterprise.systems.items():
        n, e = system.rsa_public
        print(f"{system.system_name}:")
        print(f"  Public Key (n): {n}")
        print(f"  Public Key (e): {e}")
        print(f"  Key Size: ~{n.bit_length()} bits\n")
    print("3. Secure Communication Demo:")
    message1 = "Employee salary report for Q3 2025"
    result1 = enterprise.facilitate_secure_communication("SYS_FINANCE", "SYS_HR", message1)
    if result1['success']:
        print(f"✓ Finance → HR Communication:")
        print(f"  Original: {result1['original_message']}")
        print(f"  Encrypted: {result1['encrypted_data']['ciphertext']}")
        print(f"  Decrypted: {result1['decrypted_message']}\n")
    message2 = "New employee onboarding - office supplies needed"
    result2 = enterprise.facilitate_secure_communication("SYS_HR", "SYS_SUPPLY", message2)
    if result2['success']:
        print(f"✓ HR → Supply Chain Communication:")
        print(f"  Original: {result2['original_message']}")
        print(f"  Encrypted: {result2['encrypted_data']['ciphertext']}")
        print(f"  Decrypted: {result2['decrypted_message']}\n")
    print("4. Diffie-Hellman Key Exchange Demo:")
    dh_result = enterprise.establish_session_key("SYS_FINANCE", "SYS_SUPPLY")
    if dh_result['success']:
        print(f"✓ Session Key Established between Finance and Supply Chain:")
        print(f"  Shared Secret Match: {dh_result['shared_secret_match']}")
        print(f"  Shared Secret: {dh_result['shared_secret']}")
        print(f"  Finance DH Public: {dh_result['dh_exchange_data']['system1_public']}")
        print(f"  Supply DH Public: {dh_result['dh_exchange_data']['system2_public']}\n")
    print("5. Key Management System Demo:")
    finance_keys = finance_system.key_manager.list_keys()
    print(f"Finance System Keys ({len(finance_keys)} total):")
    for key in finance_keys:
        print(f"  Key ID: {key['key_id']}")
        print(f"  Type: {key['key_type']}")
        print(f"  Status: {key['status']}")
        print(f"  Expires: {key['expires_at']}\n")
    if finance_keys:
        key_to_revoke = finance_keys[0]['key_id']
        success = finance_system.key_manager.revoke_key(key_to_revoke)
        print(f"✓ Key Revocation Demo:")
        print(f"  Revoked Key: {key_to_revoke}")
        print(f"  Success: {success}")
        revoked_key = finance_system.key_manager.retrieve_key(key_to_revoke)
        print(
            f"  Retrieval after revocation: {'Failed (as expected)' if revoked_key is None else 'Unexpected success'}\n")
demonstrate_system()
