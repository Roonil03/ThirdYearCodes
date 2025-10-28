from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import pickle

# Dataset
docs = {
    1: "data security encryption",
    2: "machine learning algorithms",
    3: "data mining techniques",
    4: "encryption decryption methods",
    5: "security protocols network",
    6: "algorithms optimization performance",
    7: "machine learning data analysis",
    8: "network security encryption",
    9: "data structures algorithms",
    10: "encryption security privacy"
}

# AES Key
key = get_random_bytes(16)

# Encryption/Decryption
def encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(str(data).encode(), 16))

def decrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), 16).decode()

# Build inverted index
index = {}
for doc_id, text in docs.items():
    for word in text.split():
        index.setdefault(word, []).append(doc_id)

# Encrypt index
enc_index = {encrypt(word, key): encrypt(doc_ids, key) for word, doc_ids in index.items()}

# Search function
def search(query, enc_index, key):
    enc_query = encrypt(query, key)
    if enc_query in enc_index:
        doc_ids = eval(decrypt(enc_index[enc_query], key))
        print(f"Query: '{query}' found in documents: {doc_ids}")
        for doc_id in doc_ids:
            print(f"  Doc {doc_id}: {docs[doc_id]}")
    else:
        print(f"Query: '{query}' not found")

# Test search
search("encryption", enc_index, key)
search("algorithms", enc_index, key)
