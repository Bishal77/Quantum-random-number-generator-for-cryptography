"""
Unit tests for qrng.runner module
Tests random bit and number generation
"""
import pytest
from qrng.runner import run_qrng_once, generate_random_bits, random_int_from_bits


class TestRunQRNGOnce:
    """Test suite for run_qrng_once function"""

    def test_basic_execution(self):
        """Test basic QRNG execution"""
        result = run_qrng_once(n_qubits=3, shots=1)
        assert isinstance(result, list)
        assert len(result) == 1

    def test_multiple_shots(self):
        """Test with multiple shots"""
        result = run_qrng_once(n_qubits=2, shots=10)
        assert len(result) == 10

    def test_bitstring_format(self):
        """Test that output bitstrings have correct format"""
        result = run_qrng_once(n_qubits=3, shots=5)
        for bitstr in result:
            assert isinstance(bitstr, str)
            assert all(c in '01' for c in bitstr)
            assert len(bitstr) == 3

    def test_different_qubit_counts(self):
        """Test with various qubit counts"""
        for n_qubits in [1, 2, 5, 10]:
            result = run_qrng_once(n_qubits=n_qubits, shots=1)
            assert len(result[0]) == n_qubits

    def test_multiple_shots_different_results(self):
        """Test that multiple shots can produce different results"""
        result = run_qrng_once(n_qubits=5, shots=100)
        # With 100 shots of 5 qubits, we should get some variety
        unique_results = set(result)
        assert len(unique_results) > 1, "Should have multiple different outcomes"


class TestGenerateRandomBits:
    """Test suite for generate_random_bits function"""

    def test_basic_generation(self):
        """Test basic random bit generation"""
        bits = generate_random_bits(target_bits=32, n_qubits=4, shots_per_call=2)
        assert isinstance(bits, str)
        assert len(bits) == 32
        assert all(c in '01' for c in bits)

    def test_different_target_lengths(self):
        """Test with various target bit lengths"""
        for target in [8, 16, 64, 256]:
            bits = generate_random_bits(target_bits=target, n_qubits=4)
            assert len(bits) == target

    def test_with_debiasing(self):
        """Test generation with Von Neumann debiasing"""
        bits = generate_random_bits(
            target_bits=32,
            n_qubits=8,
            shots_per_call=1,
            unbiased=True
        )
        assert len(bits) == 32
        assert all(c in '01' for c in bits)

    def test_without_debiasing(self):
        """Test generation without Von Neumann debiasing"""
        bits = generate_random_bits(
            target_bits=32,
            n_qubits=8,
            shots_per_call=1,
            unbiased=False
        )
        assert len(bits) == 32
        assert all(c in '01' for c in bits)

    def test_large_key_generation(self):
        """Test generation of cryptographic key size"""
        bits = generate_random_bits(target_bits=256, n_qubits=8, shots_per_call=5)
        assert len(bits) == 256

    def test_randomness_variety(self):
        """Test that generated bits have variety"""
        bits = generate_random_bits(target_bits=128, n_qubits=8)
        ones_count = bits.count('1')
        zeros_count = bits.count('0')
        # Should have both 0s and 1s
        assert ones_count > 0
        assert zeros_count > 0
        # Roughly balanced (allow 30-70 range)
        ratio = ones_count / (ones_count + zeros_count)
        assert 0.3 < ratio < 0.7

    def test_multiple_generations_different(self):
        """Test that multiple generations produce different results"""
        bits1 = generate_random_bits(target_bits=64, n_qubits=8)
        bits2 = generate_random_bits(target_bits=64, n_qubits=8)
        # Statistically, these should be different
        assert bits1 != bits2


class TestRandomIntFromBits:
    """Test suite for random_int_from_bits function"""

    def test_basic_conversion(self):
        """Test basic bitstring to integer conversion"""
        assert random_int_from_bits('0') == 0
        assert random_int_from_bits('1') == 1

    def test_binary_conversion(self):
        """Test binary to decimal conversion"""
        assert random_int_from_bits('10') == 2
        assert random_int_from_bits('11') == 3
        assert random_int_from_bits('100') == 4

    def test_larger_numbers(self):
        """Test conversion of larger numbers"""
        assert random_int_from_bits('1111') == 15
        assert random_int_from_bits('10000000') == 128
        assert random_int_from_bits('11111111') == 255

    def test_leading_zeros(self):
        """Test handling of leading zeros"""
        assert random_int_from_bits('0001') == 1
        assert random_int_from_bits('0010') == 2
        assert random_int_from_bits('0000') == 0

    def test_all_ones(self):
        """Test all-ones bitstring"""
        for length in range(1, 10):
            bitstr = '1' * length
            expected = (2 ** length) - 1
            assert random_int_from_bits(bitstr) == expected

    def test_all_zeros(self):
        """Test all-zeros bitstring"""
        for length in range(1, 10):
            bitstr = '0' * length
            assert random_int_from_bits(bitstr) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
