# qrng/circuit.py
from qiskit import QuantumCircuit

def build_qrng(num_outcomes: int):
    """
    Build a Quantum Random Number Generator circuit.

    Args:
        num_outcomes (int): Number of possible random outcomes (n).

    Returns:
        QuantumCircuit: A circuit that prepares a superposition state.
        int: Number of qubits used.
    """
    # Find smallest k such that 2^k >= num_outcomes
    k = 1
    while (1 << k) < num_outcomes:
        k += 1

    # Create circuit with k qubits and k classical bits
    qc = QuantumCircuit(k, k)

    # Apply Hadamard gates to all qubits to create superposition
    for q in range(k):
        qc.h(q)

    # Barrier for clarity
    qc.barrier()

    # Measure all qubits
    qc.measure(range(k), range(k))

    return qc, k


