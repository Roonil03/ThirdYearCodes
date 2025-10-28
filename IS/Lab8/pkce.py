from phe import paillier

# Dataset
docs = {
    1: "cloud computing security",
    2: "machine learning models",
    3: "cloud storage encryption",
    4: "security privacy protection",
    5: "machine learning cloud",
    6: "encryption algorithms security",
    7: "privacy data protection",
    8: "cloud security models",
    9: "computing distributed systems",
    10: "encryption cloud security"
}

# Generate Paillier keypair
public_key, private_key = paillier.generate_paillier_keypair()

# Build inverted index
index = {}
for doc_id, text in docs.items():
    for word in text.split():
        index.setdefault(word, []).append(doc_id)

# Encrypt index (encrypt document IDs)
enc_index = {}
for word, doc_ids in index.items():
    enc_word = public_key.encrypt(hash(word))
    enc_doc_ids = [public_key.encrypt(doc_id) for doc_id in doc_ids]
    enc_index[hash(word)] = enc_doc_ids

# Search function
def search(query):
    query_hash = hash(query)
    if query_hash in enc_index:
        enc_doc_ids = enc_index[query_hash]
        doc_ids = [private_key.decrypt(enc_id) for enc_id in enc_doc_ids]
        print(f"\nQuery: '{query}' found in documents: {doc_ids}")
        for doc_id in doc_ids:
            print(f"  Doc {doc_id}: {docs[doc_id]}")
    else:
        print(f"\nQuery: '{query}' not found")

# User input
while True:
    query = input("\nEnter search query (or 'exit' to quit): ").strip()
    if query.lower() == 'exit':
        break
    search(query)
