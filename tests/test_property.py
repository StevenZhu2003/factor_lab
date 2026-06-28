"""
Randomised tests for recursive integer factorisation.

This module performs simple property-based tests by generating random
products of small prime numbers and verifying that FactorLab recovers
the original prime factors correctly.

The tests complement the deterministic unit tests by exercising many
different factorisation trees, including repeated prime factors, while
remaining fast enough for continuous integration.
"""

from random import choices, sample

from gmpy2 import mpz

from factorlab.factor import factor

PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97,
]


def test_random_distinct_products() -> None:
    """Random products of distinct primes should factor correctly."""

    for _ in range(1000):
        primes = sample(PRIMES, k=5)

        n = mpz(1)

        for p in primes:
            n *= p

        assert factor(n) == sorted(map(mpz, primes))


def test_random_repeated_products() -> None:
    """Random products with repeated primes should factor correctly."""

    for _ in range(1000):
        primes = choices(PRIMES, k=5)

        n = mpz(1)

        for p in primes:
            n *= p

        assert factor(n) == sorted(map(mpz, primes))
