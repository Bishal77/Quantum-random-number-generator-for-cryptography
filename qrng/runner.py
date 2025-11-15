# qrng/runner.py
from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.visualization import plot_histogram
import random

from qrng.circuit import build_qrng

def run_qrng(num_outcomes: int, shots: int = 1, visualize: bool = False):
    """
    Run the Quantum Random Number Generator circuit.

    Args:
        num_outcomes (int): Number of possible random outcomes (n).
        shots (int): Number of times to run the circuit.
        visualize (bool): If True, show histogram of results.

    Returns:
        int: A random number between 0 and num_outcomes-1.
    """
    # Build the circuit
    qc, k = build_qrng(num_outcomes)

    # Use Aer simulator
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)

    # Run the circuit
    result = simulator.run(compiled_circuit, shots=shots).result()
    counts = result.get_counts()

    if visualize:
        plot_histogram(counts).show()

    # Convert bitstrings to integers
    outcomes = [int(bitstring, 2) for bitstring in counts.keys()]

    # Filter to valid outcomes (0 to num_outcomes-1)
    valid_outcomes = [o for o in outcomes if o < num_outcomes]

    # Pick one random outcome from the measurement results
    return random.choice(valid_outcomes)
