# Lab Exercises:
1. Execute the following for SSE:
    - Create a dataset: Generate a text corpus of at least ten documents. Each document should contain multiple words.
    - Implement encryption and decryption functions: Use the AES encryption and decryption functions.
    - Create an inverted index: Build an inverted index mapping word to the list of document IDs containing those words.
        - Encrypt the index using the provided encryption function.
    - Implement the search function:
        - Take a search query as input.
        - Encrypt the query.
        - Search the encrypted index for matching terms.
        - Decrypt the returned document IDs and display the corresponding documents
2. Execute the following for PKSE:
    - Create a dataset:
        - Generate a text corpus of at least ten documents. Each document should contain multiple words.
    - Implement encryption and decryption functions:
        - Use the Paillier cryptosystem for encryption and decryption.
    - Create an encrypted index:
        - Build an inverted index mapping word to the list of document IDs containing those words.
        - Encrypt the index using the Paillier cryptosystem.
    - Implement the search function:
        - Take a search query as input.
        - Encrypt the query using the public key.
        - Search the encrypted index for matching terms.
        - Decrypt the returned document IDs using the private key.
# Additional Questions:
1. Demonstrate how to securely store and transmit data using GnuPG. Additionally, show how to create a digital signature for the data and verify the signature after transmission.
2. Configure and use Snort as a Network Intrusion Detection System (NIDS) to monitor real-time network traffic. Capture network traffic, apply Snort rules, and analyze the logs to identify any potential intrusions.