# app/core/rsa_math.py
# RSA mathematics from scratch (educational)

import random
from typing import Tuple


# 1. Greatest Common Divisor
def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


# 2. Extended Euclidean Algorithm
def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y


# 3. Modular inverse
def mod_inverse(e: int, phi: int) -> int:
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Inverse does not exist")
    return x % phi


# 4. Square-and-multiply (modular exponentiation)
def pow_mod(base: int, exponent: int, modulus: int) -> int:
    result = 1
    base = base % modulus

    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus

    return result


# 5. Primality test (simple)
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


# 6. Generate prime number
def generate_prime(bits: int = 16) -> int:
    while True:
        candidate = random.getrandbits(bits)
        if is_prime(candidate):
            return candidate


# 7. Generate RSA key pair
def generate_rsa_keys(bits: int = 16):
    p = generate_prime(bits)
    q = generate_prime(bits)

    while p == q:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    if gcd(e, phi) != 1:
        e = 3

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


# 8. Encrypt / Decrypt
def encrypt(message: int, public_key: tuple) -> int:
    e, n = public_key
    return pow_mod(message, e, n)


def decrypt(ciphertext: int, private_key: tuple) -> int:
    d, n = private_key
    return pow_mod(ciphertext, d, n)
