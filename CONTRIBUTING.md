# Contributing to QRNG

Thank you for your interest in contributing to the Quantum Random Number Generator project! This document provides guidelines and instructions for contributing.

## 🎯 Getting Started

### Prerequisites

- Python 3.9+
- Git
- Familiarity with quantum computing concepts (helpful but not required)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Dhakal-Unique/quantum-random-number-generator.git
cd quantum-random-number-generator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest tests/ -v
```

## 📋 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clean, documented code
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Include type hints

### 3. Add Tests

- Write unit tests for new functions
- Test edge cases
- Ensure tests pass: `pytest tests/ -v`

### 4. Code Quality Checks

```bash
# Format with black
black qrng/

# Check with flake8
flake8 qrng/

# Type checking
mypy qrng/
```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: description of your changes"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- Provide clear description of changes
- Link any related issues
- Ensure CI/CD checks pass

## 📁 Project Structure

```
quantum-random-number-generator/
├── README.md                      # Project documentation
├── LICENSE.md                     # MIT License
├── CONTRIBUTING.md               # This file
├── requirements.txt              # Python dependencies
├── .github/
│   └── workflows/
│       └── tests.yml            # CI/CD workflow
├── qrng/
│   ├── __init__.py              # Package initialization
│   ├── circuit.py               # Quantum circuit construction
│   ├── runner.py                # Random number generation
│   ├── utils.py                 # Utility functions
│   ├── crypto.py                # AES encryption/decryption
│   ├── analysis.py              # Entropy and randomness analysis
│   └── demo.py                  # Interactive demonstration
└── tests/
    ├── test_circuit.py          # Circuit tests
    ├── test_runner.py           # Runner tests
    ├── test_utils.py            # Utility tests
    └── test_crypto.py           # Crypto tests
```

## 🔍 Code Style Guide

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`

### Documentation

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Longer description explaining what the function does,
    how it works, and any important details.

    Args:
        param1 (str): Description of param1
        param2 (int): Description of param2

    Returns:
        bool: Description of return value

    Raises:
        ValueError: Description of when this is raised

    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

## 🧪 Testing Guidelines

### Writing Tests

- Use descriptive test names: `test_<function>_<scenario>`
- Test both happy paths and edge cases
- Use pytest fixtures for setup/teardown
- Aim for >80% code coverage

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=qrng --cov-report=html

# Run specific test file
pytest tests/test_circuit.py -v

# Run specific test
pytest tests/test_circuit.py::TestBuildHadamardCircuit::test_circuit_creation_basic -v
```

## 🐛 Bug Reports

### When Reporting Bugs

1. Use a clear, descriptive title
2. Describe the exact steps to reproduce
3. Provide example code
4. Specify your Python version and OS
5. Include error messages and stack traces

### Example Bug Report

```
Title: Von Neumann debiasing removes too many bits

Description:
When running von_neumann_unbias on certain bitstrings,
it removes more bits than expected.

Steps to Reproduce:
1. Call von_neumann_unbias with bitstring '00110011'
2. Observe output length

Expected: Some output bits
Actual: Empty string

Environment:
- Python 3.11
- qrng version 1.0.0
```

## 🚀 Feature Requests

### Suggesting Enhancements

1. Use a clear, descriptive title
2. Explain the motivation
3. Provide example use cases
4. List any related issues

### Example Feature Request

```
Title: Add support for different quantum backends

Description:
Currently only supports Aer simulator. Add support for:
- IBMQ quantum hardware
- Other simulators
- Custom backends

Use Case:
Running on real quantum computers for validation
```

## 📊 Areas for Contribution

### High Priority

- [ ] Real quantum hardware support
- [ ] Advanced error mitigation techniques
- [ ] Performance optimization
- [ ] Additional statistical tests

### Medium Priority

- [ ] Extended documentation
- [ ] More encryption algorithms
- [ ] Visualization tools
- [ ] Benchmarking suite

### Low Priority

- [ ] README translations
- [ ] Additional examples
- [ ] Jupyter notebooks
- [ ] Tutorial videos

## 🏆 Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- README acknowledgements
- Release notes

## 📞 Questions?

- Open an issue on GitHub
- Check existing documentation
- Review examples in `qrng/demo.py`

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy contributing! 🚀**
