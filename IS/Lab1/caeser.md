## Attack Type: 
Known-plaintext attack on a shift (Caesar) cipher.

John used the fact that “CIW” decrypts to “yes” to recover the shift key (4), then applied that same key to the new ciphertext.

## Recovery of Key:
Ciphertext “CIW” → Plaintext “yes”
C→y implies shift key = (C_index – y_index) mod 26 = (2 – 24) mod 26 = 4.

## Decrypting “XVIEWYWI”:
Applying a shift of –4 (decrypting):
X→T, V→R, I→E, E→A, W→S, Y→U, W→S, I→E

Plaintext: `TREASURE`