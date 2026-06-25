# Factor Lab

An educational implementation of classical integer factorisation algorithms in Python.

This project focuses on understanding how classical integer factorisation algorithms work by implementing them from scratch, rather than relying on existing libraries. The goal is to provide clean, readable, and well-documented implementations suitable for learning and experimentation.

## Features

Current progress:

- Trial Division

- Miller–Rabin Primality Test

- Pollard's Rho

- Pollard's p−1

- Elliptic Curve Method (ECM)

- Quadratic Sieve (QS)

Future goals:

- Performance benchmarking

- Algorithm visualisation

- Educational examples and explanations

- Comparison with existing factorisation software

## Installation

### Using uv (recommended)

```bash
uv sync
```

### Using venv + pip

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Philosophy

This project prioritises:

- Readability over extreme optimisation.

- Educational value over raw performance.

- Modular implementations that can be studied independently.

## License

This project is released under the MIT License.
