"""
Unit tests for qrng.circuit module
Tests quantum circuit construction and execution
"""
import pytest
from qrng.circuit import build_hadamard_circuit, run_circuit_and_get_counts


class TestBuildHadamardCircuit:
    """Test suite for build_hadamard_circuit function"""

    def test_circuit_creation_basic(self):
        """Test that circuit is created successfully"""
        qc = build_hadamard_circuit(n_qubits=3)
        assert qc is not None
        assert qc.num_qubits == 3

    def test_circuit_with_measurement(self):
        """Test circuit with measurement gates"""
        qc = build_hadamard_circuit(n_qubits=2, measure=True)
        assert qc.num_qubits == 2
        assert qc.num_clbits == 2
        # Check that measurement gates are included
        assert len(qc) > 0

    def test_circuit_without_measurement(self):
        """Test circuit without measurement gates"""
        qc = build_hadamard_circuit(n_qubits=2, measure=False)
        assert qc.num_qubits == 2
        assert qc.num_clbits == 0

    def test_different_qubit_counts(self):
        """Test circuit creation with various qubit counts"""
        for n in [1, 2, 5, 10]:
            qc = build_hadamard_circuit(n_qubits=n)
            assert qc.num_qubits == n

    def test_circuit_has_hadamard_gates(self):
        """Verify Hadamard gates are applied"""
        qc = build_hadamard_circuit(n_qubits=3, measure=False)
        # Count H gates in the circuit
        h_count = sum(1 for instr in qc.data if instr[0].name == 'h')
        assert h_count == 3, "Should have 3 Hadamard gates"


class TestRunCircuitAndGetCounts:
    """Test suite for run_circuit_and_get_counts function"""

    def test_circuit_execution_single_shot(self):
        """Test circuit execution with single shot"""
        qc = build_hadamard_circuit(n_qubits=2, measure=True)
        counts = run_circuit_and_get_counts(qc, shots=1)
        assert isinstance(counts, dict)
        assert sum(counts.values()) == 1

    def test_circuit_execution_multiple_shots(self):
        """Test circuit execution with multiple shots"""
        qc = build_hadamard_circuit(n_qubits=2, measure=True)
        shots = 100
        counts = run_circuit_and_get_counts(qc, shots=shots)
        assert isinstance(counts, dict)
        assert sum(counts.values()) == shots

    def test_bitstring_format(self):
        """Test that counts keys are bitstrings"""
        qc = build_hadamard_circuit(n_qubits=3, measure=True)
        counts = run_circuit_and_get_counts(qc, shots=100)
        for bitstring in counts.keys():
            assert isinstance(bitstring, str)
            assert all(c in '01' for c in bitstring)
            assert len(bitstring) == 3

    def test_single_qubit_outcomes(self):
        """Test that single qubit produces 0 and 1"""
        qc = build_hadamard_circuit(n_qubits=1, measure=True)
        counts = run_circuit_and_get_counts(qc, shots=1000)
        # Should have both '0' and '1' with ~50% each
        assert '0' in counts or '1' in counts
        total = sum(counts.values())
        for count in counts.values():
            ratio = count / total
            # Allow some statistical variation
            assert 0.3 < ratio < 0.7, "Distribution should be roughly 50-50"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
