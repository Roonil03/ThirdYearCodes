from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

def generate_keys(bits=2048):
    key = RSA.generate(bits)
    return key.publickey(), key

def encrypt_message(plaintext: bytes, pubkey: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(pubkey)
    return cipher.encrypt(plaintext)

def decrypt_message(ciphertext: bytes, privkey: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(privkey)
    return cipher.decrypt(ciphertext)

def sign_message(message: bytes, privkey: RSA.RsaKey) -> bytes:
    h = SHA256.new(message)
    signature = pkcs1_15.new(privkey).sign(h)
    return signature

def verify_signature(message: bytes, signature: bytes, pubkey: RSA.RsaKey) -> bool:
    h = SHA256.new(message)
    try:
        pkcs1_15.new(pubkey).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

def demo_cia():
    public_key, private_key = generate_keys()
    msg = b"Sensitive data protected via RSA"

    ciphertext = encrypt_message(msg, public_key)
    decrypted = decrypt_message(ciphertext, private_key)
    assert decrypted == msg
    print("Confidentiality: decrypted matches original")

    signature = sign_message(msg, private_key)
    assert verify_signature(msg, signature, public_key), "Signature verification failed!"
    print("Integrity & Authenticity: signature verified successfully")

    print("\n--- RSA Encryption & Signing Demo ---")
    print("Original Message:", msg)
    print("Encrypted (hex):", ciphertext.hex()[:60] + "…")
    print("Signature (hex):", signature.hex()[:60] + "…")
    print("Decrypted Message:", decrypted)

if __name__ == "__main__":
    demo_cia()
