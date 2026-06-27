"""
Unit tests for recursive integer factorisation.
"""

import pytest
from gmpy2 import mpz

from factorlab.factor import factor


def test_invalid_input() -> None:
    """Values smaller than 1 should raise ValueError."""
    with pytest.raises(ValueError):
        factor(mpz(0))


def test_one() -> None:
    """1 has no prime factors."""
    assert factor(mpz(1)) == []


def test_prime() -> None:
    """Prime numbers should return themselves."""
    assert factor(mpz(97)) == [mpz(97)]


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (mpz(2), [mpz(2)]),
        (mpz(15), [mpz(3), mpz(5)]),
        (mpz(21), [mpz(3), mpz(7)]),
        (mpz(35), [mpz(5), mpz(7)]),
        (mpz(77), [mpz(7), mpz(11)]),
        (mpz(91), [mpz(7), mpz(13)]),
        (mpz(143), [mpz(11), mpz(13)]),
        (mpz(360), [mpz(2), mpz(2), mpz(2), mpz(3), mpz(3), mpz(5)]),
        (mpz(8051), [mpz(83), mpz(97)]),
        (mpz(10403), [mpz(101), mpz(103)]),
    ],
)
def test_factorisation(n: mpz, expected: list[mpz]) -> None:
    """Composite numbers should be completely factorised."""
    assert factor(n) == expected


def test_large_prime_power() -> None:
    """Prime powers should preserve multiplicity."""
    assert factor(mpz(2**10)) == [mpz(2)] * 10
