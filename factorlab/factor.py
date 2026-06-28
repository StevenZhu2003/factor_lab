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

from factorlab.pollard_rho import pollard_rho
from factorlab.primality import is_prime
from factorlab.trial_division import trial_division

logger = logging.getLogger(__name__)


def factor(n: mpz, _root: bool = True) -> list[mpz]:
    """
    Compute the complete prime factorisation of a positive integer.

    Parameters
    ----------
    n : mpz
        Positive integer to be factorised.

    _root : bool, optional
        Internal flag indicating whether this is the top-level call.

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

    result: list[mpz] = []

    #
    # Stage 1: Trial division
    #
    small_factors, remaining = trial_division(n)

    if small_factors:
        result.extend(small_factors)

        logging.info(
            "[Trial Division] Found %d small factor(s).",
            len(small_factors),
        )

    if remaining == 1:
        result.sort()

        if _root:
            logging.info(
                "[Factor] Complete factorisation of %s.",
                n,
            )

        return result

    #
    # Stage 2: Remaining number is prime
    #
    if is_prime(remaining):
        result.append(remaining)
        result.sort()

        if _root:
            logging.info(
                "[Factor] Complete factorisation of %s.",
                n,
            )

        return result

    #
    # Stage 3: Pollard Rho
    #
    left = pollard_rho(remaining)
    right = remaining // left

    logging.info(
        "[Factor] Split %s into %s × %s.",
        remaining,
        left,
        right,
    )

    logging.info(
        "[Factor] Left divisor %s is %s.",
        left,
        "prime" if is_prime(left) else "composite",
    )

    logging.info(
        "[Factor] Right divisor %s is %s.",
        right,
        "prime" if is_prime(right) else "composite",
    )

    logging.info("")

    result.extend(factor(left, _root=False))
    result.extend(factor(right, _root=False))

    result.sort()

    if _root:
        logging.info(
            "[Factor] Complete factorisation of %s.",
            n,
        )

    return result
