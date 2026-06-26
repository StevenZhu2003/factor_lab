"""
Unit tests for Pollard's Rho integer factorisation algorithm.
"""

import pytest
from gmpy2 import mpz
import random

random.seed(0)

from factorlab.pollard_rho import pollard_rho


def test_invalid_input() -> None:
    """Values smaller than 2 should raise ValueError."""
    with pytest.raises(ValueError):
        pollard_rho(mpz(1))


def test_even_number() -> None:
    """Even numbers should immediately return 2."""
    assert pollard_rho(mpz(100)) == mpz(2)


def test_prime_number() -> None:
    """Prime numbers should be returned unchanged."""
    n = mpz(101)
    assert pollard_rho(n) == n


@pytest.mark.parametrize(
    "n",
    [
        mpz(15),      # 3 × 5
        mpz(21),      # 3 × 7
        mpz(35),      # 5 × 7
        mpz(77),      # 7 × 11
        mpz(91),      # 7 × 13
        mpz(143),     # 11 × 13
        mpz(8051),    # 83 × 97
        mpz(10403),   # 101 × 103
    ],
)
def test_composite_numbers(n: mpz) -> None:
    """Returned value should be a non-trivial factor."""
    factor = pollard_rho(n)

    assert factor > 1
    assert factor < n
    assert n % factor == 0


def test_randomised_stability() -> None:
    """
    Pollard Rho is probabilistic.
    Run it repeatedly to ensure it consistently finds a valid factor.
    """
    n = mpz(8051)

    for _ in range(100):
        factor = pollard_rho(n)

        assert factor > 1
        assert factor < n
        assert n % factor == 0
