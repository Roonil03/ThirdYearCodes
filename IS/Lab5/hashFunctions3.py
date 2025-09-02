import hashlib
import random
import string
import time
from collections import defaultdict

def generate_random_strings(n: int, length: int = 16) -> list[str]:
    """
    Generate a list of n random alphanumeric strings of given length.
    """
    alphabet = string.ascii_letters + string.digits
    return [
        ''.join(random.choices(alphabet, k=length))
        for _ in range(n)
    ]

def compute_hashes(strings: list[str], algorithm: str) -> tuple[dict[str, str], float]:
    """
    Compute hashes for a list of strings using the specified algorithm,
    and return a mapping from string to hex digest, plus the total compute time.
    """
    hash_func = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256
    }[algorithm]
    
    start = time.perf_counter()
    result = {s: hash_func(s.encode('utf-8')).hexdigest() for s in strings}
    duration = time.perf_counter() - start
    return result, duration

def detect_collisions(digests: dict[str, str]) -> dict[str, list[str]]:
    """
    Given a mapping from input string to its digest, return a mapping
    from digest to list of inputs that share that digest (only collisions).
    """
    inverse = defaultdict(list)
    for s, d in digests.items():
        inverse[d].append(s)
    # Keep only digests with more than one input
    return {digest: strs for digest, strs in inverse.items() if len(strs) > 1}

def main():

    # Testing
    # 1. Generate dataset size between 50 and 100
    n = random.randint(50, 100)
    print(f"Generating {n} random strings")
    dataset = generate_random_strings(n, length=32)
    
    # 2. Compute hashes and measure time
    stats = {}
    all_hashes = {}
    for algo in ('md5', 'sha1', 'sha256'):
        digests, duration = compute_hashes(dataset, algo)
        stats[algo] = duration
        all_hashes[algo] = digests
        print(f"{algo.upper():<6}: Computation time = {duration*1000:.3f} ms")
    
    # 3. Collision detection
    print("\nCollision Detection Results:")
    for algo in ('md5', 'sha1', 'sha256'):
        collisions = detect_collisions(all_hashes[algo])
        if collisions:
            print(f"- {algo.upper()}: {len(collisions)} distinct colliding digests")
            for digest, inputs in collisions.items():
                print(f"    Digest {digest}: {inputs}")
        else:
            print(f"- {algo.upper()}: No collisions detected")
    
if __name__ == "__main__":
    main()
