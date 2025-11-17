#!/usr/bin/env python3
# qrng/demo.py
"""
Demo: Generate a quantum random key and use it for AES encryption/decryption.

This demonstrates the cryptography theme of the QRNG hackathon:
1. Generate truly random bits using quantum circuits
2. Derive an AES encryption key from quantum bits
3. Encrypt a sample message
4. Decrypt to verify the key works correctly

Run: python -m qrng.demo --key-bits 256 --n-qubits 6 --shots 1 --unbiased
"""
from .runner import generate_random_bits, random_int_from_bits
from .crypto import (
    generate_aes_key_from_bits,
    generate_aes_key_from_bits_kdf,
    aes_encrypt,
    aes_decrypt,
    bytes_to_hex,
)
import argparse


def main():
    """Main entry point for the demo script."""
    parser = argparse.ArgumentParser(
        description="Quantum Random Number Generator + AES Encryption Demo"
    )
    parser.add_argument(
        '--key-bits',
        type=int,
        default=256,
        help='Key length in bits (128/192/256) [default: 256]'
    )
    parser.add_argument(
        '--n-qubits',
        type=int,
        default=6,
        help='Qubits per shot (gives n_qubits raw bits per shot) [default: 6]'
    )
    parser.add_argument(
        '--shots',
        type=int,
        default=1,
        help='Shots per backend call [default: 1]'
    )
    parser.add_argument(
        '--unbiased',
        action='store_true',
        help='Apply Von Neumann debiasing to quantum measurements'
    )
    parser.add_argument(
        '--message',
        type=str,
        default="Hello from QRNG! This is a demo message.",
        help='Message to encrypt [default: Hello from QRNG!...]'
    )
    parser.add_argument(
        '--use-kdf',
        action='store_true',
        help='Use HKDF-based key derivation for non-predictable real-world keys'
    )
    parser.add_argument(
        '--fast-sim',
        action='store_true',
        help='Use statevector-probability fast sampling for simulator (much faster for many shots)'
    )
    args = parser.parse_args()

    print("=" * 70)
    print("🔐 Quantum Random Number Generator + AES Encryption Demo")
    print("=" * 70)

    # Step 1: Generate quantum random bits
    print(f"\n📊 Generating {args.key_bits}-bit quantum key...")
    print(f"   Parameters:")
    print(f"   - Qubits per shot: {args.n_qubits}")
    print(f"   - Shots per call: {args.shots}")
    print(f"   - Von Neumann debiasing: {args.unbiased}")

    bits = generate_random_bits(
        target_bits=args.key_bits,
        n_qubits=args.n_qubits,
        shots_per_call=args.shots,
        unbiased=args.unbiased,
        use_prob_sampling=args.fast_sim
    )
    print(f"   ✓ Generated {len(bits)} bits")

    # Step 2: Create AES key from quantum bits
    print(f"\n🔑 Deriving AES key from quantum bits...")
    key = generate_aes_key_from_bits(bits, key_size_bits=args.key_bits)
    if args.use_kdf:
        # derive using HKDF and show salt
        key, salt_hex = generate_aes_key_from_bits_kdf(bits, key_size_bits=args.key_bits)
        print(f"   Key (hex): {bytes_to_hex(key)}")
        print(f"   KDF salt (hex): {salt_hex}")
    else:
        key = generate_aes_key_from_bits(bits, key_size_bits=args.key_bits)
        print(f"   Key (hex): {bytes_to_hex(key)}")

    # Step 3: Encrypt message
    print(f"\n🔒 Encrypting message...")
    message = args.message.encode()
    print(f"   Plaintext: {message.decode()}")

    enc = aes_encrypt(key, message)
    print(f"   IV (hex):        {enc['iv']}")
    print(f"   Ciphertext (hex): {enc['ciphertext']}")

    # Step 4: Decrypt to verify
    print(f"\n🔓 Decrypting message...")
    decrypted = aes_decrypt(key, enc['iv'], enc['ciphertext'])
    print(f"   Decrypted: {decrypted.decode()}")

    # Verification
    if decrypted == message:
        print(f"\n✅ Encryption/Decryption successful!")
    else:
        print(f"\n❌ Encryption/Decryption failed!")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
