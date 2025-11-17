"""
Unit tests for qrng.utils module
Tests utility functions for bitstring manipulation and debiasing
"""
import pytest
from qrng.utils import qiskit_bitstring_order, bits_from_counts, von_neumann_unbias


class TestQiskitBitstringOrder:
    """Test suite for qiskit_bitstring_order function"""

    def test_basic_reversal(self):
        """Test basic bitstring reversal"""
        assert qiskit_bitstring_order('10') == '01'
        assert qiskit_bitstring_order('01') == '10'

    def test_single_bit(self):
        """Test single bit handling"""
        assert qiskit_bitstring_order('0') == '0'
        assert qiskit_bitstring_order('1') == '1'

    def test_longer_bitstring(self):
        """Test longer bitstrings"""
        assert qiskit_bitstring_order('1010') == '0101'
        assert qiskit_bitstring_order('11110000') == '00001111'

    def test_all_zeros(self):
        """Test all zeros"""
        assert qiskit_bitstring_order('0000') == '0000'

    def test_all_ones(self):
        """Test all ones"""
        assert qiskit_bitstring_order('1111') == '1111'

    def test_idempotent(self):
        """Test that applying twice returns original"""
        original = '101010'
        twice = qiskit_bitstring_order(qiskit_bitstring_order(original))
        assert twice == original


class TestBitsFromCounts:
    """Test suite for bits_from_counts function"""

    def test_single_outcome(self):
        """Test with single measurement outcome"""
        counts = {'00': 5}
        result = bits_from_counts(counts)
        assert len(result) == 5
        # Results should be reversed due to qiskit_bitstring_order
        assert all(b == '00' for b in result)

    def test_multiple_outcomes(self):
        """Test with multiple measurement outcomes"""
        counts = {'10': 3, '01': 2}
        result = bits_from_counts(counts)
        assert len(result) == 5
        # Count occurrences after order correction
        assert len([b for b in result if b == '01']) == 3  # '10' -> '01'
        assert len([b for b in result if b == '10']) == 2  # '01' -> '10'

    def test_empty_counts(self):
        """Test with empty counts dict"""
        counts = {}
        result = bits_from_counts(counts)
        assert len(result) == 0

    def test_total_count_preserved(self):
        """Test that total count is preserved"""
        counts = {'00': 10, '11': 20, '01': 15}
        result = bits_from_counts(counts)
        assert len(result) == 45

    def test_order_correction(self):
        """Test that bitstring order is corrected"""
        counts = {'01': 1}  # Qiskit format
        result = bits_from_counts(counts)
        # Should be converted to '10' in natural order
        assert result[0] == '10'


class TestVonNeumannUnbias:
    """Test suite for von_neumann_unbias function"""

    def test_basic_01_pair(self):
        """Test 01 pair becomes 0"""
        result = von_neumann_unbias('01')
        assert result == '0'

    def test_basic_10_pair(self):
        """Test 10 pair becomes 1"""
        result = von_neumann_unbias('10')
        assert result == '1'

    def test_00_pair_discarded(self):
        """Test 00 pair is discarded"""
        result = von_neumann_unbias('00')
        assert result == ''

    def test_11_pair_discarded(self):
        """Test 11 pair is discarded"""
        result = von_neumann_unbias('11')
        assert result == ''

    def test_mixed_bitstring(self):
        """Test mixed bitstring with valid and invalid pairs"""
        # 01 10 00 11 -> 0 1 '' ''
        result = von_neumann_unbias('01100011')
        assert result == '01'

    def test_multiple_pairs(self):
        """Test multiple consecutive valid pairs"""
        result = von_neumann_unbias('01011010')  # 01 01 10 10
        assert result == '0010'

    def test_odd_length_bitstring(self):
        """Test odd length bitstring (last bit ignored)"""
        result = von_neumann_unbias('0101')  # 01 01, no trailing bit
        assert result == '00'

    def test_empty_string(self):
        """Test empty string"""
        result = von_neumann_unbias('')
        assert result == ''

    def test_single_bit(self):
        """Test single bit (should be ignored)"""
        result = von_neumann_unbias('1')
        assert result == ''

    def test_debiasing_produces_less_output(self):
        """Test that debiasing typically produces less output than input"""
        bitstring = '0101010101010101'  # All valid pairs
        result = von_neumann_unbias(bitstring)
        # Should produce 8 bits from 16 bits (50% efficiency)
        assert len(result) == 8

    def test_high_bias_string(self):
        """Test string with many invalid pairs"""
        # 00 11 00 11 00 11 -> all discarded
        result = von_neumann_unbias('001100110011')
        assert result == ''


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
