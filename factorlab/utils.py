"""
Common mathematical utilities for integer factorisation algorithms.
"""

from gmpy2 import mpz


def decompose(n: mpz) -> tuple[int, mpz]:
    """
    Decompose a positive integer into

        n = 2^s * d

    where d is odd.

    Parameters
    ----------
    n : mpz
        Positive integer.

    Returns
    -------
    tuple[int, mpz]
        (s, d)
    """

    if n <= 0:
        raise ValueError("n must be positive")

    s = 0
    d = n

    while d % 2 == 0:
        s += 1
        d //= 2

    return s, d
