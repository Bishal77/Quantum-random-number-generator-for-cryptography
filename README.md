# Quantum Random Number Generator (QRNG)

## 📌 Overview
This repository contains our Hackathon 2025 project: a **Quantum Random Number Generator (QRNG)** built using Qiskit.  
Unlike classical random number generators, which rely on deterministic algorithms, this project leverages **quantum superposition and measurement** to produce truly random outcomes.

## 🎯 Hackathon Prompt
Random number generators are essential for computing, especially in security and cryptography.  
Classical generators are pseudo-random, but quantum systems can produce truly random outcomes.  

**Your challenge:**  
- Create a quantum circuit that generates random numbers.  
- Decide the number of qubits and possible outcomes (`n`).  
- Use **Hadamard (H) gates** to prepare a superposition state with `n` equally likely outcomes.  
- Map measured states to numeric values so your program prints a random number.


## 🧑‍💻 Getting Started
1. Clone the repo:
   ```bash
   git clone https://github.com/Dhakal-Unique/quantum-random-number-generator.git
   cd quantum-random-number-generator



---

### 4. **Usage Example**
```markdown
## ▶️ Usage Example
```python
from qrng.runner import run_qrng

# Generate a random number with 3 qubits and 100 shots
result = run_qrng(num_outcomes=8, shots=100)
print("Random number:", result)
```






### 5. **Tips & Deeper Questions**
```markdown
## 💡 Tips
- Run once (single shot) → one random number.  
- Run multiple shots → shows fairness of distribution.  
- Noise may bias results → explore error mitigation.

## 🔍 Deeper Questions
- Why do some values appear more often?  
- Which error mitigation techniques make results fairer?

## 🏆 Hackathon Judging Criteria
1. **Technical Aspects (30 pts)** – Algorithm complexity, optimization, scalability, Qiskit usage.  
2. **Originality (25 pts)** – Novelty, creativity, difficulty attempted.  
3. **Usefulness (25 pts)** – Practicality, design quality, real-world applications.  
4. **Presentation (20 pts)** – Clarity, storytelling, team collaboration.


## 📚 Suggested Resources
- Basics of Quantum Information  
- Quantum Magic Eight Ball    
- Error Mitigation and Suppression Techniques Documentation

## 📂 Project Structure
qrng-hackathon/
├── README.md
├── LICENSE.md
├── requirements.txt
└── qrng/
    ├── circuit.py
    └── runner.py



## 📜 License
This project is licensed under the **MIT License** _- see the [LICENSE.md](LICENSE.md) file for details.

