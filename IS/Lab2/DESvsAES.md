Testing message: 'Performance Testing of Encryption Algorithms'  
Message length: 44 characters  
DES padded length: 48 bytes  
AES padded length: 48 bytes  
Running 1 iterations for accurate timing...

============================================================
# PERFORMANCE COMPARISON RESULTS
============================================================      
Algorithm    Encrypt (ms)    Decrypt (ms)    Total (ms)  
------------------------------------------------------------    
DES          0.087500        0.035800        0.123300    
AES-256      0.014100        0.018700        0.032800    

============================================================
# PERFORMANCE ANALYSIS
============================================================  
Encryption Speed: AES-256 is 6.2x faster than DES  
Decryption Speed: AES-256 is 1.9x faster than DES  
Overall Speed: AES-256 is 3.8x faster than DES  

============================================================  
# CORRECTNESS VERIFICATION
============================================================  
Original message: 'Performance Testing of Encryption Algorithms'  
DES decrypted: 'Performance Testing of Encryption Algorithms'  
AES-256 decrypted: 'Performance Testing of Encryption Algorithms'  
DES verification: ✓ PASS  
AES-256 verification: ✓ PASS  

============================================================
# CIPHERTEXT INFORMATION
============================================================  
DES Ciphertext (hex):   `af2ffa09206340b18c1f07e33cc8129cda008f367b4974ac314f5fa2b7814e5a848dbab80107043a7fe6e3494d72feb3`  
AES-256 Ciphertext (hex):   `ac1dc462ea00ffad16cee96424fa315e0d4367cee9a25a862c9d8412e170768a6c632acf7c7350bf5d6fba79b933ccfa`  
DES Ciphertext length: 48 bytes  
AES-256 Ciphertext length: 48 bytes  