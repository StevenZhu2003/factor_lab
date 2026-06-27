"""
Recursive integer factorisation.

This module provides the high-level recursive factorisation routine
built on top of the algorithms implemented in FactorLab.

The current implementation combines:

    • Miller–Rabin probabilistic primality testing
    • Pollard's Rho integer factorisation

to recursively decompose an arbitrary positive integer into its prime
factors.

The recursive process terminates whenever a prime number is reached,
as determined by the Miller–Rabin primality test. Composite numbers
are split into two smaller factors using Pollard's Rho algorithm until
the complete prime factorisation is obtained.

This module serves as the primary public interface of the library.
Future factorisation algorithms (e.g. Pollard p−1, ECM, Quadratic
Sieve, or GNFS) can be integrated transparently without changing the
external API.
"""

from gmpy2 import mpz

from factorlab.primality import is_prime
from factorlab.pollard_rho import pollard_rho


def factor(n: mpz) -> list[mpz]:
    """
    Compute the complete prime factorisation of a positive integer.

    Parameters
    ----------
    n : mpz
        Positive integer to be factorised.

    Returns
    -------
    list[mpz]
        Prime factors of n in ascending order.

    Raises
    ------
    ValueError
        If n < 1.
    """
    
    if n < 1:
        raise ValueError("n must be a positive integer")

    if n == 1:
        return []

    if is_prime(n):
        return [n]

    d = pollard_rho(n)

    left = factor(d)
    right = factor(n // d)

    result = left + right
    result.sort()

    return result
