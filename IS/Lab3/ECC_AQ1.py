from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import os

pt = "Secure Transactions"


def generate_ecc_keys():
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()
    return private_key, public_key


def aes_encrypt(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padding_length = 16 - (len(data) % 16)
    padded_data = data + bytes([padding_length] * padding_length)

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext


def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    padding_length = padded_data[-1]
    return padded_data[:-padding_length]


def ecc_encrypt(message, public_key):
    ephemeral_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    ephemeral_public = ephemeral_private.public_key()

    shared_key = ephemeral_private.exchange(ec.ECDH(), public_key)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'ECC encryption',
        backend=default_backend()
    ).derive(shared_key)

    encrypted_message = aes_encrypt(message.encode(), derived_key)

    ephemeral_public_bytes = ephemeral_public.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )

    return ephemeral_public_bytes, encrypted_message


def ecc_decrypt(ephemeral_public_bytes, encrypted_message, private_key):
    ephemeral_public = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), ephemeral_public_bytes
    )

    shared_key = private_key.exchange(ec.ECDH(), ephemeral_public)
    derived_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'ECC encryption',
        backend=default_backend()
    ).derive(shared_key)

    decrypted_data = aes_decrypt(encrypted_message, derived_key)
    return decrypted_data.decode()


private_key, public_key = generate_ecc_keys()

print(f"Plaintext: {pt}")
print(f"Curve: SECP256R1")

private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(f"Private key size: {len(private_bytes)} bytes")
print(f"Public key size: {len(public_bytes)} bytes")

ephemeral_public_bytes, ct = ecc_encrypt(pt, public_key)
print(f"Ephemeral public key (hex): {ephemeral_public_bytes.hex()}")
print(f"Ciphertext (hex): {ct.hex()}")
print(f"Ciphertext length: {len(ct)} bytes")

mes = ecc_decrypt(ephemeral_public_bytes, ct, private_key)
print(f"Decrypted message: {mes}")

print(f"Original == Decrypted: {pt == mes}")
