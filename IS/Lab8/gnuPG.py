import gnupg

gpg = gnupg.GPG()

# Generate key pair
input_data = gpg.gen_key_input(key_type="RSA", key_length=2048, name_email=input("Enter your email: "))
key = gpg.gen_key(input_data)
print(f"\nKey generated: {key}")

# Get recipient email
recipient = input("Enter recipient email: ")

# Encrypt and sign data
message = input("Enter message to encrypt: ")
encrypted = gpg.encrypt(message, recipient, sign=key, always_trust=True)
print(f"\nEncrypted & Signed:\n{encrypted}")

# Decrypt and verify
decrypted = gpg.decrypt(str(encrypted), always_trust=True)
print(f"\nDecrypted: {decrypted}")
print(f"Signature valid: {decrypted.valid}")
print(f"Signed by: {decrypted.username}")
