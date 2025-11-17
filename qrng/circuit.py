"""Quantum circuit helpers for the QRNG package.

Provides helpers to build a Hadamard circuit and run it on the Aer
simulator. Includes a small transpile cache and an optional fast
simulator sampling path (sample from statevector probabilities).
"""

from typing import Dict, Tuple

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

# Single Aer simulator instance reused across calls to reduce overhead
BACKEND = AerSimulator()

# Cache for transpiled circuits. Keyed by circuit metadata + optimization
# level to avoid repeated transpilation of identical circuits.
_TRANSPILED_CACHE: Dict[Tuple[int, int, int, Tuple[Tuple[str, int], ...], int], QuantumCircuit] = {}


def build_hadamard_circuit(n_qubits: int, measure: bool = True) -> QuantumCircuit:
    """Return an n-qubit circuit with Hadamard on each qubit.

    When ``measure`` is True the circuit will include classical
    registers and measurements. Otherwise the circuit is unitary only.
    """
    if measure:
        qc = QuantumCircuit(n_qubits, n_qubits)
    else:
        qc = QuantumCircuit(n_qubits)

    for q in range(n_qubits):
        qc.h(q)

    if measure:
        qc.measure(range(n_qubits), range(n_qubits))

    return qc


def run_circuit_and_get_counts(
    qc: QuantumCircuit,
    shots: int = 1,
    optimization_level: int = 3,
    use_prob_sampling: bool = False,
) -> dict:
    """Run ``qc`` on the Aer simulator and return measurement counts.

    - Reuses a cached transpiled circuit when possible.
    - If ``use_prob_sampling`` is True, obtains the statevector and
      samples locally from the probability distribution (fast for many
      shots; simulator-only).
    """
    ops = tuple(sorted(qc.count_ops().items()))
    cache_key = (qc.num_qubits, qc.num_clbits, qc.depth(), ops, optimization_level)

    t_qc = _TRANSPILED_CACHE.get(cache_key)
    if t_qc is None:
        t_qc = transpile(qc, BACKEND, optimization_level=optimization_level)
        _TRANSPILED_CACHE[cache_key] = t_qc

    if use_prob_sampling:
        # Request statevector and sample locally
        job = BACKEND.run(t_qc, shots=1, method="statevector")
        result = job.result()
        # different Aer versions expose get_statevector with/without args
        try:
            sv = result.get_statevector(t_qc)
        except TypeError:
            sv = result.get_statevector()

        probs = np.abs(np.asarray(sv)) ** 2
        probs /= probs.sum()
        indices = np.random.choice(len(probs), size=shots, p=probs)

        counts = {}
        for idx in indices:
            bitstr = format(int(idx), f"0{qc.num_qubits}b")
            counts[bitstr] = counts.get(bitstr, 0) + 1
        return counts

    job = BACKEND.run(t_qc, shots=shots)
    result = job.result()
    return result.get_counts()


