# Quick Start Guide

Get started with Quantum Random Number Generator in 5 minutes!

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/Dhakal-Unique/quantum-random-number-generator.git
cd quantum-random-number-generator

# Install dependencies
pip install -r requirements.txt
```

## ⚡ 5-Minute Tutorial

### 1. Generate Random Bits

```python
from qrng.runner import generate_random_bits

# Generate 32 random bits
bits = generate_random_bits(target_bits=32, n_qubits=6, unbiased=True)
print(f"Random bits: {bits}")
print(f"Length: {len(bits)}")
```

### 2. Generate Encryption Key

```python
from qrng.runner import generate_random_bits
from qrng.crypto import generate_aes_key_from_bits, bytes_to_hex

# Generate 256-bit encryption key
bits = generate_random_bits(target_bits=256, n_qubits=8, unbiased=True)
key = generate_aes_key_from_bits(bits, key_size_bits=256)
print(f"Quantum key: {bytes_to_hex(key)}")
```

### 3. Encrypt and Decrypt

```python
from qrng.crypto import aes_encrypt, aes_decrypt

# Encrypt
message = b"Secret message"
encrypted = aes_encrypt(key, message)
print(f"Encrypted: {encrypted['ciphertext']}")

# Decrypt
decrypted = aes_decrypt(key, encrypted['iv'], encrypted['ciphertext'])
print(f"Decrypted: {decrypted.decode()}")
```

### 4. Run Interactive Demo

```bash
# Basic demo
python -m qrng.demo

# With custom parameters
python -m qrng.demo --key-bits 256 --n-qubits 6 --shots 2 --unbiased
```

### 5. Analyze Randomness

```python
from qrng.runner import generate_random_bits
from qrng.analysis import analyze_bitstring

bits = generate_random_bits(target_bits=256, n_qubits=8)
results = analyze_bitstring(bits, verbose=True)
```

## 📚 Common Tasks

### Generate Different Key Sizes

```python
# 128-bit key (lightweight)
bits_128 = generate_random_bits(target_bits=128, n_qubits=4)

# 192-bit key (medium)
bits_192 = generate_random_bits(target_bits=192, n_qubits=6)

# 256-bit key (strong)
bits_256 = generate_random_bits(target_bits=256, n_qubits=8)
```

### Test Randomness Quality

```python
from qrng.analysis import analyze_bitstring

# Generate test bits
bits = generate_random_bits(target_bits=1024, n_qubits=8)

# Full analysis with report
results = analyze_bitstring(bits, verbose=True)

# Access specific metrics
print(f"Shannon entropy: {results['shannon_entropy']}")
print(f"Bit distribution: {results['bit_distribution']}")
print(f"Chi-square test: {results['chi_square_test']}")
```

### Batch Random Number Generation

```python
# Generate multiple independent keys
keys = []
for i in range(10):
    bits = generate_random_bits(target_bits=256, n_qubits=8, unbiased=True)
    key = generate_aes_key_from_bits(bits)
    keys.append(key)
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=qrng --cov-report=html

# Run specific test file
pytest tests/test_crypto.py -v
```

## 🔧 Troubleshooting

### Issue: ImportError for qiskit

**Solution**: Install qiskit properly

```bash
pip install qiskit qiskit-aer
```

### Issue: Tests failing

**Solution**: Ensure all dependencies are installed

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### Issue: Slow random number generation

**Solution**: Reduce n_qubits or shots_per_call

```python
# Faster but potentially less random
bits = generate_random_bits(target_bits=256, n_qubits=4, shots_per_call=1)
```

## 📖 Next Steps

1. **Read Full Documentation**: See `README.md`
2. **Explore Code**: Check out `qrng/` modules
3. **Contribute**: See `CONTRIBUTING.md`
4. **Try Advanced Features**: Use `qrng/analysis.py` for quality metrics

## 🎯 Key Concepts

### Hadamard Gates

Create quantum superposition on qubits - foundation of quantum randomness

### Von Neumann Debiasing

Removes bias from quantum measurements for truly random bits

### AES Encryption

Uses quantum bits for cryptographically secure encryption keys

### Entropy Analysis

Measures randomness quality with multiple statistical tests

## 🚀 What's Next?

- Explore `demo.py` for advanced examples
- Check `analysis.py` for randomness metrics
- Review tests for usage patterns
- Read paper for theoretical background

---

**Ready to generate quantum random numbers? Start coding! 🎉**
