from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii

pt = "Secure Transactions"

curve = registry.get_curve('brainpoolP256r1')

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)

def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext

print(f"Plaintext: {pt}")

privKey = secrets.randbelow(curve.field.n)
pubKey = privKey * curve.g

print(f"Private key: {hex(privKey)}")
print(f"Public key (x): {hex(pubKey.x)}")
print(f"Public key (y): {hex(pubKey.y)}")
print(f"Curve: {curve.name}")

encryptedMsg = encrypt_ECC(pt.encode(), pubKey)
ct = binascii.hexlify(encryptedMsg[0]).decode()
print(f"Ciphertext (hex): {ct}")
print(f"Nonce (hex): {binascii.hexlify(encryptedMsg[1]).decode()}")
print(f"Auth Tag (hex): {binascii.hexlify(encryptedMsg[2]).decode()}")

mes = decrypt_ECC(encryptedMsg, privKey).decode()
print(f"Decrypted message: {mes}")

print(f"Original == Decrypted: {pt == mes}")
