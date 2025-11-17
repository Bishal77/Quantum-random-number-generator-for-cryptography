"""High-level QRNG runner utilities.

Provides functions to run a Hadamard circuit and collect random bits.
The fast-path (``use_prob_sampling``) can be used with simulators to
sample directly from the statevector probabilities for improved
throughput when many shots are required.
"""

from typing import List

from .circuit import build_hadamard_circuit, run_circuit_and_get_counts
from .utils import bits_from_counts, von_neumann_unbias


def run_qrng_once(n_qubits: int, shots: int = 1, use_prob_sampling: bool = False) -> List[str]:
    """Run one Hadamard circuit and return measured bitstrings.

    Returns a list of bitstrings (one per shot) in MSB->LSB order.
    """
    qc = build_hadamard_circuit(n_qubits, measure=True)
    counts = run_circuit_and_get_counts(qc, shots=shots, use_prob_sampling=use_prob_sampling)
    return bits_from_counts(counts)


def generate_random_bits(
    target_bits: int,
    n_qubits: int = 5,
    shots_per_call: int = 1,
    unbiased: bool = True,
    use_prob_sampling: bool = False,
) -> str:
    """Generate at least ``target_bits`` random bits and return exact length.

    The generator builds a single circuit and reuses a cached transpiled
    version to reduce overhead across repeated calls.
    """
    collected: List[str] = []
    qc = build_hadamard_circuit(n_qubits, measure=True)

    while len("".join(collected)) < target_bits:
        counts = run_circuit_and_get_counts(qc, shots=shots_per_call, use_prob_sampling=use_prob_sampling)
        measured_list = bits_from_counts(counts)
        raw = "".join(measured_list)

        if unbiased:
            extracted = von_neumann_unbias(raw)
            if extracted:
                collected.append(extracted)
        else:
            collected.append(raw)

    return ("".join(collected))[:target_bits]


def random_int_from_bits(bitstr: str) -> int:
    """Convert a binary string to an integer value."""
    return int(bitstr, 2)
