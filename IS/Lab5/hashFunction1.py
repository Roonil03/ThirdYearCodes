def djb2_hash(input_string):
    hash_value = 5381
    mask_32bit = 0xFFFFFFFF
    for char in input_string:
        ascii_val = ord(char)
        hash_value = ((hash_value << 5) + hash_value + ascii_val) & mask_32bit
    return hash_value


def demonstrate_hash_properties():
    print("DJB2 Hash Function Implementation")
    print("=" * 60)
    print("Demonstrating Cryptographic Hash Function Properties")
    print("=" * 60)
    test_inputs = [
        "hello",
        "world",
        "Hello",  # Case sensitivity
        "hello world",  # Spaces
        "Python",  # Mixed case
        "cryptography",  # Longer string
        "hash function",  # Multiple words
        "A",  # Single character
        "",  # Empty string
        "12345",  # Numeric string
        "!@#$%",  # Special characters
        "The quick brown fox jumps over the lazy dog"  # Long sentence
    ]
    print(f"{'Input String':<35} {'Hash (Hex)':<12} {'Hash (Decimal)':<12}")
    print("-" * 65)
    for test_input in test_inputs:
        hash_result = djb2_hash(test_input)
        print(f"{repr(test_input):<35} {hex(hash_result):<12} {hash_result:<12}")
    print("\n" + "=" * 60)
    print("Avalanche Effect Demonstration")
    print("=" * 60)
    print("Small changes in input should produce significantly different hashes")
    avalanche_tests = [
        "test",
        "Test",  # Case change
        "test1",  # Character addition
        "tes",  # Character removal
        "tests",  # Character addition at end
        "tesa"  # Character substitution
    ]
    print(f"{'Input':<10} {'Hash (Hex)':<12} {'Binary (last 16 bits)':<18}")
    print("-" * 45)
    for test_str in avalanche_tests:
        hash_val = djb2_hash(test_str)
        binary_repr = format(hash_val & 0xFFFF, '016b')
        print(f"{repr(test_str):<10} {hex(hash_val):<12} {binary_repr}")
    print("\n" + "=" * 60)
    print("Hash Distribution Analysis")
    print("=" * 60)
    distribution_hashes = []
    for i in range(20):
        test_str = f"data{i:02d}"
        hash_val = djb2_hash(test_str)
        distribution_hashes.append(hash_val)
        if i < 10:  # Show first 10 for brevity
            print(f"Hash of '{test_str}': {hex(hash_val)}")
    print(f"\nDistribution Statistics (20 samples):")
    print(f"Min hash value: {min(distribution_hashes):,}")
    print(f"Max hash value: {max(distribution_hashes):,}")
    print(f"Range: {max(distribution_hashes) - min(distribution_hashes):,}")
    print(f"Average: {sum(distribution_hashes) // len(distribution_hashes):,}")
    print("\n" + "=" * 60)
    print("Collision Resistance Property")
    print("=" * 60)
    print("Finding two inputs with the same hash should be computationally difficult")
    collision_tests = [
        ("password", "Password"),
        ("abc123", "abc124"),
        ("hello", "world"),
        ("data", "date")
    ]
    for input1, input2 in collision_tests:
        hash1 = djb2_hash(input1)
        hash2 = djb2_hash(input2)
        print(f"'{input1}' -> {hex(hash1)}")
        print(f"'{input2}' -> {hex(hash2)}")
        print(f"Different: {hash1 != hash2}\n")

def hash_performance_test():
    import time
    print("=" * 60)
    print("Performance Analysis")
    print("=" * 60)
    test_lengths = [10, 100, 1000, 5000]
    for length in test_lengths:
        test_string = "a" * length
        start_time = time.time()
        hash_result = djb2_hash(test_string)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000
        print(f"String length {length:4d}: Hash = {hex(hash_result)} "
              f"(Time: {execution_time:.4f} ms)")

if __name__ == "__main__":
    demonstrate_hash_properties()
    hash_performance_test()