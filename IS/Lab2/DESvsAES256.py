from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
from time import perf_counter
import statistics

def performance_test(message, iterations=1000):
    # Setup keys
    key_des = b'A1B2C3D4'  # 8 bytes for DES
    key_aes256 = bytes.fromhex('0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF')

    cipher_des = DES.new(key_des, DES.MODE_ECB)
    cipher_aes256 = AES.new(key_aes256, AES.MODE_ECB)

    padded_message_des = pad(message.encode(), DES.block_size)
    padded_message_aes = pad(message.encode(), AES.block_size)

    print(f"Testing message: '{message}'")
    print(f"Message length: {len(message)} characters")
    print(f"DES padded length: {len(padded_message_des)} bytes")
    print(f"AES padded length: {len(padded_message_aes)} bytes")
    print(f"Running {iterations} iterations for accurate timing...\n")

    des_encrypt_times = []
    des_decrypt_times = []
    aes_encrypt_times = []
    aes_decrypt_times = []

    for _ in range(iterations):
        start = perf_counter()
        ciphertext_des = cipher_des.encrypt(padded_message_des)
        des_encrypt_times.append(perf_counter() - start)

        start = perf_counter()
        decrypted_des = unpad(cipher_des.decrypt(ciphertext_des), DES.block_size).decode()
        des_decrypt_times.append(perf_counter() - start)

        start = perf_counter()
        ciphertext_aes = cipher_aes256.encrypt(padded_message_aes)
        aes_encrypt_times.append(perf_counter() - start)

        start = perf_counter()
        decrypted_aes = unpad(cipher_aes256.decrypt(ciphertext_aes), AES.block_size).decode()
        aes_decrypt_times.append(perf_counter() - start)

    # For display, re-generate output from the last run
    ciphertext_des = cipher_des.encrypt(padded_message_des)
    decrypted_des = unpad(cipher_des.decrypt(ciphertext_des), DES.block_size).decode()
    ciphertext_aes = cipher_aes256.encrypt(padded_message_aes)
    decrypted_aes = unpad(cipher_aes256.decrypt(ciphertext_aes), AES.block_size).decode()

    # Calculate statistics
    des_avg_encrypt = statistics.mean(des_encrypt_times) * 1000
    des_avg_decrypt = statistics.mean(des_decrypt_times) * 1000
    aes_avg_encrypt = statistics.mean(aes_encrypt_times) * 1000
    aes_avg_decrypt = statistics.mean(aes_decrypt_times) * 1000

    print("="*60)
    print("PERFORMANCE COMPARISON RESULTS")
    print("="*60)
    print(f"{'Algorithm':<12} {'Encrypt (ms)':<15} {'Decrypt (ms)':<15} {'Total (ms)':<12}")
    print("-" * 60)
    print(f"{'DES':<12} {des_avg_encrypt:<15.6f} {des_avg_decrypt:<15.6f} {des_avg_encrypt + des_avg_decrypt:<12.6f}")
    print(f"{'AES-256':<12} {aes_avg_encrypt:<15.6f} {aes_avg_decrypt:<15.6f} {aes_avg_encrypt + aes_avg_decrypt:<12.6f}")

    encrypt_ratio = des_avg_encrypt / aes_avg_encrypt if aes_avg_encrypt > 0 else 0
    decrypt_ratio = des_avg_decrypt / aes_avg_decrypt if aes_avg_decrypt > 0 else 0
    total_ratio = (des_avg_encrypt + des_avg_decrypt) / (aes_avg_encrypt + aes_avg_decrypt) if (aes_avg_encrypt + aes_avg_decrypt) > 0 else 0

    print("\n" + "="*60)
    print("PERFORMANCE ANALYSIS")
    print("="*60)
    print(f"Encryption Speed: AES-256 is {encrypt_ratio:.1f}x faster than DES")
    print(f"Decryption Speed: AES-256 is {decrypt_ratio:.1f}x faster than DES")
    print(f"Overall Speed: AES-256 is {total_ratio:.1f}x faster than DES")

    print("\n" + "="*60)
    print("CORRECTNESS VERIFICATION")
    print("="*60)
    print(f"Original message: '{message}'")
    print(f"DES decrypted: '{decrypted_des}'")
    print(f"AES-256 decrypted: '{decrypted_aes}'")
    print(f"DES verification: {'✓ PASS' if decrypted_des == message else '✗ FAIL'}")
    print(f"AES-256 verification: {'✓ PASS' if decrypted_aes == message else '✗ FAIL'}")

    print("\n" + "="*60)
    print("CIPHERTEXT INFORMATION")
    print("="*60)
    print(f"DES Ciphertext (hex): {ciphertext_des.hex()}")
    print(f"AES-256 Ciphertext (hex): {ciphertext_aes.hex()}")
    print(f"DES Ciphertext length: {len(ciphertext_des)} bytes")
    print(f"AES-256 Ciphertext length: {len(ciphertext_aes)} bytes")

    return {
        'des_encrypt_avg': des_avg_encrypt,
        'des_decrypt_avg': des_avg_decrypt,
        'aes_encrypt_avg': aes_avg_encrypt,
        'aes_decrypt_avg': aes_avg_decrypt,
        'encrypt_ratio': encrypt_ratio,
        'decrypt_ratio': decrypt_ratio,
        'total_ratio': total_ratio
    }

if __name__ == "__main__":
    message = "Performance Testing of Encryption Algorithms"
    results = performance_test(message, iterations=1)