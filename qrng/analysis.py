"""
Entropy and randomness analysis module
Provides tools to measure the quality of generated random numbers
"""
import math
from collections import Counter
from typing import Dict, Tuple


def shannon_entropy(bitstring: str) -> float:
    """
    Calculate Shannon entropy of a bitstring.
    
    Shannon entropy H = -Σ(p_i * log2(p_i)) for each bit value
    Maximum entropy is 1.0 for perfectly random binary data.
    
    Args:
        bitstring (str): Binary string to analyze.
    
    Returns:
        float: Shannon entropy value (0.0 to 1.0).
    """
    if not bitstring:
        return 0.0
    
    # Count occurrences of each bit
    counts = Counter(bitstring)
    length = len(bitstring)
    
    entropy = 0.0
    for count in counts.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    
    return entropy


def min_entropy(bitstring: str) -> float:
    """
    Calculate min-entropy of a bitstring.
    
    Min-entropy H_inf = -log2(max(p_i))
    Useful for worst-case analysis.
    
    Args:
        bitstring (str): Binary string to analyze.
    
    Returns:
        float: Min-entropy value.
    """
    if not bitstring:
        return 0.0
    
    counts = Counter(bitstring)
    max_prob = max(counts.values()) / len(bitstring)
    
    if max_prob == 0:
        return float('inf')
    return -math.log2(max_prob)


def bit_distribution(bitstring: str) -> Dict[str, float]:
    """
    Calculate the distribution of 0s and 1s.
    
    Args:
        bitstring (str): Binary string to analyze.
    
    Returns:
        dict: Mapping {'0': proportion_of_zeros, '1': proportion_of_ones}
    """
    if not bitstring:
        return {'0': 0.0, '1': 0.0}
    
    counts = Counter(bitstring)
    length = len(bitstring)
    
    return {
        '0': counts.get('0', 0) / length,
        '1': counts.get('1', 0) / length,
    }


def runs_test(bitstring: str) -> Tuple[int, float]:
    """
    Perform runs test on a bitstring.
    
    A "run" is a maximal sequence of identical bits.
    Used to detect patterns and deviations from randomness.
    
    Args:
        bitstring (str): Binary string to analyze.
    
    Returns:
        tuple: (number_of_runs, runs_expected_for_random_sequence)
    """
    if len(bitstring) < 2:
        return 1, 1.0
    
    # Count runs
    runs = 1
    for i in range(1, len(bitstring)):
        if bitstring[i] != bitstring[i-1]:
            runs += 1
    
    # Expected runs for random sequence
    n = len(bitstring)
    zeros = bitstring.count('0')
    ones = bitstring.count('1')
    
    if zeros == 0 or ones == 0:
        return runs, float('nan')
    
    expected_runs = (2 * zeros * ones) / n + 1
    
    return runs, expected_runs


def hamming_weight(bitstring: str) -> Tuple[int, float]:
    """
    Calculate the Hamming weight (number of 1s) and its ratio.
    
    Args:
        bitstring (str): Binary string to analyze.
    
    Returns:
        tuple: (number_of_ones, proportion_of_ones)
    """
    if not bitstring:
        return 0, 0.0
    
    ones = bitstring.count('1')
    return ones, ones / len(bitstring)


def autocorrelation(bitstring: str, lag: int = 1) -> float:
    """
    Calculate autocorrelation at given lag.
    
    Autocorrelation measures if bits are correlated with themselves at a lag.
    Random bits should have near-zero autocorrelation.
    
    Args:
        bitstring (str): Binary string to analyze.
        lag (int): Lag for autocorrelation calculation.
    
    Returns:
        float: Autocorrelation value (-1.0 to 1.0)
    """
    if len(bitstring) <= lag:
        return 0.0
    
    # Convert to numeric: '0' -> -1, '1' -> 1 (for better statistics)
    bits_numeric = [1 if b == '1' else -1 for b in bitstring]
    
    n = len(bits_numeric) - lag
    if n == 0:
        return 0.0
    
    # Calculate correlation
    mean = sum(bits_numeric) / len(bits_numeric)
    
    numerator = sum(
        (bits_numeric[i] - mean) * (bits_numeric[i + lag] - mean)
        for i in range(n)
    )
    
    denominator = sum((b - mean) ** 2 for b in bits_numeric)
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def chi_square_test(bitstring: str) -> Tuple[float, float]:
    """
    Perform chi-square test for uniformity.
    
    Tests if the distribution of 0s and 1s is significantly different
    from the expected 50-50 distribution.
    
    Args:
        bitstring (str): Binary string to analyze.
    
    Returns:
        tuple: (chi_square_statistic, expected_statistic_for_random)
    """
    if not bitstring:
        return 0.0, 0.0
    
    n = len(bitstring)
    zeros = bitstring.count('0')
    ones = bitstring.count('1')
    
    # Expected count for each value
    expected = n / 2
    
    # Chi-square statistic
    chi_square = ((zeros - expected) ** 2 + (ones - expected) ** 2) / expected
    
    # For 1 degree of freedom, critical value at 0.05 significance is ~3.841
    return chi_square, 3.841


def analyze_bitstring(bitstring: str, verbose: bool = True) -> Dict:
    """
    Comprehensive analysis of a bitstring's randomness properties.
    
    Args:
        bitstring (str): Binary string to analyze.
        verbose (bool): If True, print results.
    
    Returns:
        dict: Dictionary containing all analysis results.
    """
    results = {
        'length': len(bitstring),
        'shannon_entropy': shannon_entropy(bitstring),
        'min_entropy': min_entropy(bitstring),
        'bit_distribution': bit_distribution(bitstring),
        'hamming_weight': hamming_weight(bitstring),
        'runs_test': runs_test(bitstring),
        'autocorrelation_lag1': autocorrelation(bitstring, lag=1),
        'autocorrelation_lag2': autocorrelation(bitstring, lag=2),
        'chi_square_test': chi_square_test(bitstring),
    }
    
    if verbose:
        print(f"\n{'='*70}")
        print(f"Randomness Analysis Report")
        print(f"{'='*70}")
        print(f"Length: {results['length']} bits")
        print(f"\nEntropy Metrics:")
        print(f"  Shannon Entropy: {results['shannon_entropy']:.4f} (max: 1.0)")
        print(f"  Min-Entropy: {results['min_entropy']:.4f}")
        
        dist = results['bit_distribution']
        print(f"\nBit Distribution:")
        print(f"  0s: {dist['0']*100:.2f}%")
        print(f"  1s: {dist['1']*100:.2f}%")
        
        hw, hw_ratio = results['hamming_weight']
        print(f"\nHamming Weight:")
        print(f"  Count: {hw} (ratio: {hw_ratio:.4f})")
        
        runs, expected_runs = results['runs_test']
        print(f"\nRuns Test:")
        print(f"  Runs: {runs} (expected for random: {expected_runs:.2f})")
        
        print(f"\nAutocorrelation:")
        print(f"  Lag-1: {results['autocorrelation_lag1']:.4f}")
        print(f"  Lag-2: {results['autocorrelation_lag2']:.4f}")
        
        chi_sq, chi_critical = results['chi_square_test']
        print(f"\nChi-Square Test:")
        print(f"  Chi-square: {chi_sq:.4f} (critical: {chi_critical:.4f})")
        if chi_sq < chi_critical:
            print(f"  Result: ✓ Pass (uniform distribution)")
        else:
            print(f"  Result: ✗ Fail (non-uniform distribution)")
        
        print(f"\n{'='*70}\n")
    
    return results


if __name__ == '__main__':
    # Example usage
    test_bitstring = '0101' * 25  # 100 bits
    analyze_bitstring(test_bitstring)
