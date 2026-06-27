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

import logging

from gmpy2 import mpz

from .pollard_rho import pollard_rho
from .primality import is_prime

logger = logging.getLogger(__name__)


def factor(n: mpz, *, _root: bool = True,) -> list[mpz]:
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

    try:
        left = pollard_rho(n)
    except RuntimeError:
        logger.warning("[Factor] Pollard Rho exhausted.")
        logger.warning(f"[Factor] Remaining composite: {n}")
        return [n]
    
    right = n // left

    logger.info(f"[Factor] Split {n} into {left} × {right}.")

    if is_prime(left):
        logger.info(f"[Factor] Left divisor {left} is prime.")
    else:
        logger.info(f"[Factor] Left divisor {left} is composite.")

    if is_prime(right):
        logger.info(f"[Factor] Right divisor {right} is prime.\n")
    else:
        logger.info(f"[Factor] Right divisor {right} is composite.\n")

    left_result = factor(left, _root=False)
    right_result = factor(right, _root=False)

    result = left_result + right_result
    result.sort()

    if _root:
        logger.info(f"[Factor] Complete factorisation of {n}.")

    return result
