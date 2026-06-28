"""
Prime Number Utilities

This module provides utilities for generating prime numbers using the
classical Sieve of Eratosthenes.

The sieve is constructed once when the module is imported. The resulting
list of prime numbers can then be reused throughout FactorLab by trial
division, Pollard's p-1, ECM, Quadratic Sieve, and other algorithms.

The default sieve limit is chosen to balance startup time and practical
utility. Future versions may make this configurable.
"""

from math import isqrt


DEFAULT_SIEVE_LIMIT = 1_000_000


def sieve(limit: int) -> list[int]:
    """
    Generate all prime numbers up to a given limit.

    Parameters
    ----------
    limit : int
        Inclusive upper bound.

    Returns
    -------
    list[int]
        All prime numbers less than or equal to ``limit``.
    """

    if limit < 2:
        return []

    is_prime = bytearray(b"\x01") * (limit + 1)

    is_prime[0] = 0
    is_prime[1] = 0

    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            is_prime[p * p : limit + 1 : p] = (
                b"\x00"
                * (((limit - p * p) // p) + 1)
            )

    return [
        p
        for p in range(2, limit + 1)
        if is_prime[p]
    ]


PRIMES = sieve(DEFAULT_SIEVE_LIMIT)
